from twitter_cred import * # enter credentials in twitter_cred.py
import logging
import tweepy as tw
from pymongo import MongoClient
import time
import re

# This example collects tweets with the hashtag "djokovic". Retweets are discarded.
query = '#djokovic -is:retweet'

def connect_mongodb():
    HOST = 'tweet_mongodb' # 127.0.0.1   0.0.0.0
    PORT = 27017
    conn_string = f"mongodb://{HOST}:{PORT}"
    mo_client = MongoClient(conn_string)
    try:
        # The ping command is cheap and does not require auth.
        mo_client.admin.command('hello')
        logging.critical('\n########################################\n\
    Connection to Mongodb Server Established\
    \n########################################\n')
    except:
        logging.critical('\n###################################\nConnection to Mongodb Server Failed\n###################################\n')
    return mo_client


def remove_emoji(text):
    '''
    Some of the emojis will be removed.
    '''
    regrex_pattern = re.compile(pattern = "["
        # u"\U0001F600-\U0001F64F"  # emoticons
        # u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        # u"\U0001F680-\U0001F6FF"  # transport & map symbols
        # u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf" # arrow up
        u"\u23e9" # arrow right
        u"\u231a" # watch
        u"\ufe0f"  # dingbats
        u"\u3030"
        u"\u2019"
        u"\u0027"
        u"\u2018"
        "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'', text)

def data_cleaning(tweet):
    '''
    The tweets are cleaned from certain characters.
    '''
    tweet = re.sub(r"RT @[\w]*:", " ", tweet) # removes RT @s
    tweet = re.sub(r'@[\w]*', " ", tweet) # removes @s
    tweet = re.sub(r'https?://[A-Za-z0-9./]*', " ", tweet) # removes http-links
    tweet = re.sub('\n', " ", tweet)
    tweet = re.sub(r'#', " ", tweet) # whole hashtag: (r'#[A-Za-z0-9./]*, " ", tweet)
    tweet = tweet.replace("$", " ")
    tweet = tweet.replace("'", " ")
    tweet = tweet.replace("/", " ")
    tweet = tweet.replace("+", " ")
    tweet = tweet.replace('&amp;', 'and')
    tweet = " ".join(tweet.split())
    tweet = remove_emoji(tweet)
    return tweet

def get_tweets(query):
    client = tw.Client(bearer_token=BEARER_TOKEN,consumer_key=API_KEY,consumer_secret=API_KEY_SECRET, access_token=ACCESS_TOKEN,access_token_secret=ACCESS_TOKEN_SECRET)
    if client:
        logging.critical("\nAutentication OK")
    else:
        logging.critical('\nVerify your credentials')
    db_tweets = connect_mongodb().tweets # creates database tweets_collection
    tweets = db_tweets.tweets_collection

    paginator = tw.Paginator(client.search_recent_tweets, tweet_fields=['lang','id','created_at','text'], query=query).flatten(limit=200)
    for tweet in paginator:
        if tweet['lang']=='en':
            text = data_cleaning(tweet.text)+" "
            new_tweet = {"text":text} #if exists no duplicates
            logging.critical(f'\n\n\nINCOMING TWEET ID {tweet.id}:\n{new_tweet}\n\n\n')
            if new_tweet == tweets.find(new_tweet):
                logging.critical('-----Tweet already in MongoDB-----')
                continue
            else: 
                tweets.insert_one(new_tweet)
                logging.critical('-----Tweet being written into MongoDB-----')

time.sleep(2)
get_tweets(query)