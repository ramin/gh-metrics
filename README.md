## Usage

Run the script using Python and pass the required and optional arguments as flags:



```
python script.py --config CONFIG_PATH --auth-token GITHUB_TOKEN [--start-date START_DATE] [--end-date END_DATE]
```



Flags:
    --config CONFIG_PATH: Path to the YAML configuration file. (required)
    --auth-token GITHUB_TOKEN: Your GitHub personal access token. (required)
    --start-date START_DATE: The start date for the analysis in the "YYYY-MM-DD" format. (optional, default is 2 weeks ago from the current date)
    --end-date END_DATE: The end date for the analysis in the "YYYY-MM-DD" format. (optional, default is the current date)

## Example:

Analyze PRs from the past two weeks (using defaults for start and end date):

```python
    python script.py --config config.yaml --auth-token YOUR_GITHUB_TOKEN
```



### Analyze PRs from specific dates:

```python
    python script.py --config config.yaml --start-date 2023-01-01 --end-date 2023-01-15 --auth-token YOUR_GITHUB_TOKEN
```



### Output

The script outputs JSON data with the following metrics:

    pr_count: Total number of PRs.
    distinct_contributors: Number of unique contributors.
    label_distribution: Distribution of labels across PRs.
    average_pr_open_time: Average time PRs stay open.
    pr_open_time_histogram: A histogram of PR open times, categorized into predefined bins.

## Security Note

Always keep your GitHub personal access tokens secure and never embed them directly in code. Use environment variables or secure vaults to handle sensitive data, especially in production environments.
