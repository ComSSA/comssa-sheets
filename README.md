# ComSSA Sheets

## Setting up Python environment
1. Install [uv](https://docs.astral.sh/uv/guides/install-python/)
2. Run `uv init` in this directory to create a project
3. Run `uv sync` to install dependencies

**NOTE:** If you want to add dependencies, use `uv add dependency` to keep the lockfile up to date
**Example:** If I want to install pandas, I would run `uv add pandas` *instead of* `pip install pandas` etc.

## Setup

1. Add `service-account.json` file and fill out environment variables in .env file (see example.env)
2. Add the service account email to your Google Sheet with editor permissions
3. Edit crontab to run every hour
`0 * * * * python3 main.py >> /path/to/log.txt 2>&1`
