import os
import json
import tweepy
import time
import pandas as pd
import re
import string
from pprint import pprint
import inspect


path = "//"
winspath = "C:/Users/hoatr/crawler/twitter/"

# Twitter credentials for the app
secrets = json.loads(open(path + "accesskey.json").read())

consumer_key = secrets["consumer_key"]
consumer_secret = secrets["consumer_secret"]
access_token = secrets["access_token"]
access_secret = secrets["access_secret"]

# Pass twitter credentials to tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


# for tweet in limit_handled(tweepy.Cursor(api.user_timeline).items(3)):
#     print(tweet.text)

for tweet in limit_handled(
    tweepy.Cursor(
        api.search, q="#i_DECIDE", count=1, lang="en", since="2020-02-10"
    ).items(1)
):
    # print(tweet)
    pprint(vars(tweet))
