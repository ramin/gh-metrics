import argparse
import yaml
import os
import pandas as pd
from pprint import pprint
from github import Github
from datetime import datetime, timedelta


def read_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config['repo_owner'], config['repo_name']


def get_pr_data(g, repo_owner, repo_name, start_date, end_date):
    maxPrs = 1000
    prcount = 0

    repo = g.get_repo(f"{repo_owner}/{repo_name}")

    prs = repo.get_pulls(state='all', base='main',
                         sort='created', direction='desc')

    pr_data = []

    for pr in prs:
        # Ensure that the time is timezone-naive
        pr_created_at = pr.created_at.replace(tzinfo=None)
        pr_closed_at = pr.closed_at.replace(
            tzinfo=None) if pr.closed_at else None  # Only non-None if PR is closed

        prcount += 1
        if prcount > maxPrs:
            break

        if pr_created_at < start_date:
            print("breaking at ", pr_created_at)
            break

        if pr_created_at >= start_date and (pr_closed_at <= end_date if pr_closed_at else True):
            pr_data.append({
                "title": pr.title,
                "number": pr.number,
                "contributor": pr.user.login,
                "created_at": pr_created_at,
                "closed_at": pr.closed_at,
                "open_time": None if pr.closed_at is None else pr.closed_at - pr.created_at,
                "labels": [label.name for label in pr.labels],
            })
        else:
            print("ignoring pr ", pr.title)

    return pd.DataFrame(pr_data)


def analyze_pr_data(df):
    analysis_result = {
        "pr_count": len(df),
        "distinct_contributors": df['contributor'].nunique(),
        "label_distribution": df['labels'].explode().value_counts().to_dict(),
        "average_pr_open_time": None,
        "pr_open_time_histogram": None,
        "open": pd.isna(df['closed_at']).sum(),
    }

    counts_by_day = df.groupby(
        df['created_at'].dt.date).size().reset_index(name='count')
    counts_by_day['created_at'] = counts_by_day['created_at'].astype(str)
    analysis_result["counts per_day"] = counts_by_day.to_dict(orient='records')

    analysis_result['average_pr_open_time'] = humanize_timedelta(
        df['open_time'].mean())

    time_bins = pd.to_timedelta([
        '1H', '2H', '3H',
        '5H', '8H', '12H',
        '1D', '3D', '7D',
    ])

    bin_labels = [
        "1_hour", "2_hours", "3_hours",
        "5_hours", "8_hours", "12_hour",
        "1_day", "3_days", "7_days"
    ]

    df['time_bin'] = pd.cut(
        df['open_time'],
        bins=time_bins,
        labels=bin_labels[:-1],
        right=False
    ).cat.add_categories(bin_labels[-1])

    analysis_result['pr_open_time_histogram'] = df['time_bin'].value_counts(
    ).to_dict()

    return analysis_result


def humanize_timedelta(td):
    """
    Convert a Timedelta object to a human-readable string.

    Parameters:
    - td: pd.Timedelta, the timedelta object to convert

    Returns:
    - str, the formatted string
    """
    # Ensure the input is a Timedelta object
    if not isinstance(td, pd.Timedelta):
        raise ValueError("Input should be a pandas Timedelta object")

    # Extracting components
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Creating a custom string
    if days > 0:
        time_str = f"{days} days {hours} hours {minutes} minutes"
    elif hours > 0:
        time_str = f"{hours} hours {minutes} minutes"
    else:
        time_str = f"{minutes} minutes"

    return time_str


def main():
    default_start_date = (
        datetime.now() - timedelta(weeks=2)).strftime("%Y-%m-%d")

    default_end_date = datetime.now().strftime("%Y-%m-%d")

    parser = argparse.ArgumentParser(
        description="Analyze PRs from a GitHub repo"
    )

    parser.add_argument("--config",
                        help="Path to the config.yaml file",
                        default="config.yml")
    parser.add_argument("--start-date",
                        help="Start date (YYYY-MM-DD)",
                        default=default_start_date)
    parser.add_argument("--end-date",
                        help="End date (YYYY-MM-DD)",
                        default=default_end_date)

    args = parser.parse_args()

    repo_owner, repo_name = read_config(args.config)

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("Please set the GITHUB_TOKEN environment variable.")

    g = Github(token)

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    pr_df = get_pr_data(
        g,
        repo_owner,
        repo_name,
        start_date,
        end_date
    )

    analysis_result = analyze_pr_data(pr_df)

    pprint(analysis_result)


if __name__ == "__main__":
    main()
