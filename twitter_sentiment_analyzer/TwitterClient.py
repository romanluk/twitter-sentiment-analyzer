import tweepy
from twitter_sentiment_analyzer.config import *

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

class TwitterClient:
    def __init__(self, listener, tracks):
        try:
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            twitterStream = Stream(auth, listener)
            twitterStream.filter(track=tracks)
        except:
            print("Error: Authentication Failed")

class TwitterStreamListener(StreamListener):
    def on_data(self, data):
        print(data)
    
    def on_error(self, status):
        print(status)