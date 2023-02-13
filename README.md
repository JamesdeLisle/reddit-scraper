# reddit-scraper

A Reddit scraping tool

We use [pmaw](https://pypi.org/project/pmaw/) to perform the scraping. `pmaw` wraps the [Pushshift](https://reddit-api.readthedocs.io/en/latest/) reddit API for searching posts and comments. `pmaw` handles the API rate limiting and cacheing automatically.

We store the results in a postgres database with a single table:
```SQL
CREATE TABLE IF NOT EXISTS posts (
    username VARCHAR(128),
    subreddit VARCHAR(128),
    is_submitter BOOLEAN,
    created_at BIGINT,
    score BIGINT,
    guilded BOOLEAN,
    body TEXT,
    body_sha1 VARCHAR(160),
    post_url VARCHAR(540),
    PRIMARY KEY (username, subreddit, created_at, body_sha1)
)
```

## Requirements

1. docker installed.
2. docker-compose installed.
3. python 3.10.x

## Usage

1. Clone this repository `git clone https://github.com/JamesdeLisle/reddit-scraper.git`
2. Navigate into the cloned directory `cd reddit-scraper`.
3. Run `docker-compose build`.
4. Run `docker-compose up`.

This will stand up a PostgreSQL database, and scrape all reddit posts made in the last 24 hours that contain the word `coronavirus`. 

Then it will wait until 24 hours have past and then repeat the process.

This will continue indefinitely.