# Dockerized data-pipeline to analyze the sentiment of tweets
![diagram](./img/tweet_analyzer_pipeline.svg)
### 1. Clone repository with:
```bash
git clone https://github.com/to-schi/tweet-analyzer-pipeline.git
```
### 2. Enter your credentials in "twitter_cred.py":
Get your API-credentials from [developer.twitter.com](https://developer.twitter.com).
```bash
nano ./tweet-analyzer-pipeline/tweet_collector/src/twitter_cred.py
# Enter your credentials and save file with ctrl-x
# Limit is set to 200 tweets
```
### 3. Enter your preferred tweet-query:
```bash
nano ./tweet-analyzer-pipeline/tweet_collector/src/tweet_collector.py
# Insert query-text in line 9: "query = '#SOME_PHRASE'" and save file with ctrl-x
```
### 4. Insert the webhook-url to your slack-channel:
```bash
nano ./tweet-analyzer-pipeline/tweet_slack/src/conf.py
# Insert webhook-url and save file with ctrl-x
```
### 5. Change directory and start docker:
```bash
cd tweet-analyzer-pipeline
sudo docker-compose up
# Add '-d' for background-mode
````

__Docker will build 5 containers and start the pipeline automatically:__
tweet_mongodb, tweet_collector, tweet_postgres, tweet_etl, and tweet_slack.

&nbsp;

This project was created during the [Spiced Academy](https://www.spiced-academy.com) Data Science Bootcamp Nov/2021.