from pymongo import MongoClient
from sqlalchemy import create_engine
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from time import sleep

sleep(10)

# MONGO-DATABASE
HOST_MDB = 'tweet_mongodb'
PORT_MDB = 27017

conn_string_mdb = f"mongodb://{HOST_MDB}:{PORT_MDB}" 
client = MongoClient(conn_string_mdb)
db_tweets = client.tweets
tweets = db_tweets.tweets_collection

## POSTGRES
USERNAME_PG = 'postgres'
PASSWORD_PG = 'postgres'
HOST_PG = 'tweet_postgres'
PORT_PG = 5432
DATABASE_NAME_PG = 'tweets'

# Connection string
conn_string_pg = f"postgresql://{USERNAME_PG}:{PASSWORD_PG}@{HOST_PG}:{PORT_PG}/{DATABASE_NAME_PG}" 
pg = create_engine(conn_string_pg, client_encoding='utf8')

pg.execute("""
CREATE TABLE IF NOT EXISTS tweets_sentiments (
    id SERIAL,
    tweettext TEXT,
    sentiment NUMERIC
);
""")

def extract():
    tweet_document_list = list(tweets.find())
    extracted = []
    for document in tweet_document_list:
        logging.critical(f"Tweet extracted: {document['text']}")
        extracted.append(document['text'])
    return extracted

def transform(tweet_text):
    s = SentimentIntensityAnalyzer()
    sentiment_score = s.polarity_scores(tweet_text)['compound']
    logging.critical("\n---TRANSFORMATION COMPLETED---")
    return tweet_text, sentiment_score

def load(tweet_transformed,sentiment_score):
    insert_query = f"""
    INSERT INTO tweets_sentiments (tweettext, sentiment)
    VALUES ('{tweet_transformed}', '{sentiment_score}');
    """
    pg.execute(insert_query)
    logging.critical(f"TWEET AND SENTIMENT {sentiment_score} LOADED INTO POSTGRES")

# Extract tweets from MongoDB, transform to sentiment-values and load into Postgres-Database
tweet_texts = extract()
for tweet in tweet_texts:
    tweet_transformed, sentiment_score = transform(tweet)
    load(tweet_transformed, sentiment_score)

select_avg = pg.execute(f"""
    SELECT AVG(sentiment) FROM tweets_sentiments;
    """).fetchall()[0][0]
logging.critical(f"Average sentiment of #Djocovic-Tweets is: {select_avg}")
'''Average sentiment of #Djocovic-Tweets is: -0.02945910285285285285'''