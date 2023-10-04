## GH Metrics

Analyze some metrics around a window of time from a github repo, as i want to track Pull requests as a means of measuring team and project harmony.

Looking at

number of PRs
time they sat open for pending review
number of distinct contributors
(using labels) what kind of PR and how many were external

## Current

- using python 3.9
- requirements.txt includes
    - yaml
    - pandas
    - PyGithub


## Usage

Ensure you've exported a github access token to `GITHUB_TOKEN`

Run the script using Python and pass the required and optional arguments as flags:

```
python script.py --config CONFIG_PATH [--start-date START_DATE] [--end-date END_DATE] [--absolute]
```

```
Flags:
    --config CONFIG_PATH: Path to the YAML configuration file. (optional)
    --start-date START_DATE: The start date for the analysis in the "YYYY-MM-DD" format. (optional, default is 2 weeks ago from the current date)
    --end-date END_DATE: The end date for the analysis in the "YYYY-MM-DD" format. (optional, default is the current date)
    --absolute (presence): generate statistics for entire history of repository
```

## Example:

Analyze PRs from the past two weeks (using defaults for start and end date):

```python
    python script.py --config config.yaml
```

### Analyze PRs from specific dates:

```python
    python script.py --config config.yaml --start-date 2023-01-01 --end-date 2023-01-15
```

### Using the `--absolute` Flag

The `--absolute` flag allows you to control whether the statistics should be generated in absolute mode or for the entire history of the repository.


### Output

The script outputs JSON data with the following metrics:

    average_pr_open_time: Average time a PR was open
    counts_per_day: PRs opened each day
    open: Remaining OPEN PRs from period
    pr_count: Total number of PRs.
    distinct_contributors: Number of unique contributors.
    label_distribution: Distribution of labels across PRs.
    average_pr_open_time: Average time PRs stay open.
    pr_open_time_histogram: A histogram of PR open times, categorized into predefined bins.

## Security Note

Always keep your GitHub personal access tokens secure and never embed them directly in code. Use environment variables or secure vaults to handle sensitive data, especially in production environments.
