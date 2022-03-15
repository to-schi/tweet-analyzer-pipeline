"""
Selects the most postive tweets and slacks them in a predefined Slack channel
"""
import logging
from sqlalchemy import create_engine
import requests
import time
import conf

time.sleep(20)
webhook_url = conf.webhook_url

USERNAME_PG = 'postgres'
PASSWORD_PG = 'postgres'
HOST_PG = 'tweet_postgres'
PORT_PG = 5432
DATABASE_NAME_PG = 'tweets'

conn_string_pg = f"postgresql://{USERNAME_PG}:{PASSWORD_PG}@{HOST_PG}:{PORT_PG}/{DATABASE_NAME_PG}" 
pg = create_engine(conn_string_pg, client_encoding='utf8')

select_query = """
SELECT * FROM tweets_sentiments
WHERE sentiment<0
ORDER BY sentiment ASC
LIMIT 4;
"""

res = pg.execute(select_query)
text = {"text": "The four most negative tweets about #Djokovic recently:"}
#requests.post(url=webhook_url, json=text)
logging.critical("-----The four most negative tweets about #Djokovic recently:-----")
for row in res:
    sentiment = str((row["sentiment"]))
    text = (row["tweettext"])
    #post = {"text": f"Sentiment: {sentiment}, Tweet: {text}"}
    #requests.post(url=webhook_url, json=post)
    logging.critical(f"Sentiment: {sentiment}, Tweet: {text}")

