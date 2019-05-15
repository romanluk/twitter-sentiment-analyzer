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
        self.twitterStream.disconnect()
        self.twitterStream.filter(track=tracks, is_async=True)

class TwitterStreamListener(StreamListener):
    def __init__(self, on_data_callback):
        self.__terminate = False
        self.on_data_callback = on_data_callback

    def terminate(self):
        self.__terminate = True

    def on_data(self, data):
        print(data)
        self.on_data_callback(data)
        return not self.__terminate

    def on_error(self, status_code):
        print("Twitter client error: status code = " + status_code)