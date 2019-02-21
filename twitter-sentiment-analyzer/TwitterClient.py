import tweepy
import config

from tweepy import OAuthHandler

class TwitterClient(object):
    def __init__(self):
        try:
            self.auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            self.tweepyAPI = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def get_tweets(self, query, count):
        tweets = []
        try:
            fetched_tweets = self.tweepyAPI.search(q = query, count = count)
            for tweet in fetched_tweets:
                if tweet.retweet_count > 0:
                    # even if tweet has retweets, append only once
                    if tweet not in tweets:
                        tweets.append(tweet)
                else:
                    tweets.append(tweet)
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))