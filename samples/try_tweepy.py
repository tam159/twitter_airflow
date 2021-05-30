# Dylan's MacbookPro #
# JP DILAN KALPA - 11634268 #
import os
import json
import pandas as pd
import tweepy
import time
import re
import string
from pprint import pprint
import inspect
from models import *
from crawler.location import location_maching
from dbutils.base import Scoped_session as session
from twitter.tweepy_api import api
from ai_modules.age_gender import age_gender_pridiction
from schemas.user import UserSchema


def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


# Attribute review
# dump(tweets[0])
# print(tweets[0].entities['urls'][0]['expanded_url'])
# print(tweets[0].__dict__)

# User infomation
# user = api.get_user(1240834732306268162)
# user = api.get_user("realDonaldTrump")
# print(user.id)
# print(user.friends)
# print(user.__dict__.keys())
# print(user.__dict__)
# print(dir(user))
# api.create_friendship("yessigreena")
# if user.protected is True and user.follow_request_sent is False:
#     api.create_friendship(user.id)
# pprint(vars(user))
# print(age_gender_pridiction(user))
# print(user.followers()[19])
# print(user.followers_ids()[29])

# Followers
# followers = api.followers("asriiiwm")
# print(len(followers))
# pprint(followers)
# pprint(vars(followers[10]))

# followers_ids = api.followers_ids("reandine")
# print(followers_ids)

# f = api.get_user(1211505960151183360)
# print(f.screen_name)
# Friends
# friends = api.friends('kwardani_retno')
# pprint(vars(followers[10]))
# friends_ids = api.friends_ids('hiip_asia')
# print(friends_ids)
# users = api.lookup_users('NpT_Dc')
# pprint(vars(users[0]))

# Home timeline
# home_tweets = api.home_timeline()
# pprint(vars(home_tweets[0]))

# tweets = tweepy.Cursor(api.home_timeline).items(1)
# for tweet in tweets:
#     print(tweet)
# print('{real_name} (@{name}) said {tweet}\n\n'.format(
#     real_name=tweet.author.name, name=tweet.author.screen_name,
#     tweet=tweet.text))

# User timeline
# tweets = api.user_timeline('50cent')
# tweets = api.user_timeline()
# pprint(vars(tweets[0]))
# for t in my_tweets:statuses
#     print(t.text)

# Status
# status = api.get_status(1225288731235700737)
# pprint(vars(status))

# Retwitters
# retweeters = api.retweeters(1225288731235700737)
# print(retweeters)
# pprint(vars(retweeters))

# Favorites
# favorites = api.favorites('npt_dc')
# pprint(vars(favorites[0]))


# me = api.me()
# print(me.screen_name)
# print(me.name)


# api.update_status("This is your tweet message")
# api.update_with_media('/mnt/data/Entertainment/Picture/Cloud.jpg',
#                       "This is your tweet message")

# media_list = []
# response = api.media_upload('/mnt/data/Entertainment/Picture/Cloud.jpg')
# media_list.append(response.media_id_string)
# api.update_status("This is your tweet message", media_ids=media_list)

# Limit Handle
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(1 * 60)


# Cursor
# for follower in limit_handled(
#     tweepy.Cursor(api.followers, screen_name="realDonaldTrump").items()
# ):
#     # if follower.friends_count < 300:
#     print(follower.screen_name)


# for follower_id in limit_handled(
#     tweepy.Cursor(api.followers_ids, screen_name="realDonaldTrump").items()
# ):
#     print(follower_id)

# Exception
# try:
#     user = api.get_user("  npt_dC  ")
#     pprint(vars(user))
# except tweepy.error.TweepError as Exception:
#     if eval(Exception.reason)[0]["message"] == "User not found.":
#         print("hehe")
