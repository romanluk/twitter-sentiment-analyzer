import tweepy
from twitter_sentiment_analyzer.config import *

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

class TwitterClient:
    def __init__(self, listener):
        try:
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            self.twitterStream = Stream(auth, listener)
        except:
            print("Error: Authentication Failed")

    def filter(self, tracks):
        self.twitterStream.filter(track=tracks)

class TwitterStreamListener(StreamListener):
    def __init__(self):
        self.terminate = False

    def on_data(self, data):
        print(data)
        return not self.terminate