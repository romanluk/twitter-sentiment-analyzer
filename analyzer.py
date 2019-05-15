import re
from textblob import TextBlob

class Analyzer():
    @staticmethod
    def analyze(text):
        analysis = TextBlob(Analyzer.__clean_tweet(text))
        print(analysis.polarity)
        positive = 0
        negative = 0
        neutral = 0
        if analysis.polarity > 0:
            positive = 1
        elif analysis.polarity < 0:
            negative = 1
        else:
            neutral = 1
        return {
            'positive' : positive,
            'negative' : negative,
            'neutral' : neutral
        }

    @staticmethod
    def determine_track(text, tracks):
        words_set = set(text.split())
        for track in tracks:
            track_set = set(track)
            if track_set & words_set:
                return track
        return None

    @staticmethod
    def __clean_tweet(tweet):
        return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())