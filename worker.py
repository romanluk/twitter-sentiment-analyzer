import time, threading
import json
from db import FirestoreDb
from entities import ReportPeriod
from analyzer import Analyzer
from twitter_sentiment_analyzer.TwitterClient import TwitterClient, TwitterStreamListener

class Worker(object):
    __instance = None

    @staticmethod
    def get_instance():
        if Worker.__instance == None:
            Worker()
        return Worker.__instance

    def __init__(self):
        if Worker.__instance != None:
            raise Exception("Worker:: constructor  called on a singleton class")
        else:
            self.REPORT_PERIOD_DURATION = 10 #seconds
            self.period_start = 0
            self.tracks = []
            self.terms_dict = {}
            self.processed_data = {}
            self.twitter_stram_listener = TwitterStreamListener(self.on_data_callback)
            self.twitter_client = TwitterClient(self.twitter_stram_listener)
            self.db = FirestoreDb.get_instance()
            Worker.__instance = self

    def __update_all_dashboards_meta(self):
        all_dashboards_meta = self.db.get_all_dashboards_meta()
        terms_dict = {}
        tracks = []
        for meta_dict in all_dashboards_meta:
            tracks.append(meta_dict.get('search_term'))
            terms_dict[meta_dict.get('search_term')] = {
                'user_id' : meta_dict.get('user_id'),
                'id' : meta_dict.get('id')
            }
        self.terms_dict = terms_dict
        self.tracks = tracks

    def update_twitter_client_tracks(self):
        self.__update_all_dashboards_meta()
        self.twitter_client.filter(self.tracks)

    def start(self):
        self.update_twitter_client_tracks()
        self.schedule_next_data_flush()
    
    def on_data_callback(self, data):
        parsedTweet = json.loads(data)
        search_term = Analyzer.determine_track(parsedTweet.get('text'), self.tracks)
        if search_term != None:
            processed = Analyzer.analyze(parsedTweet.get('text'))
            processed_data_value = self.processed_data.get(search_term)
            if processed_data_value:
                self.processed_data.update({
                    search_term : {
                        'positive' : processed_data_value.get('positive', 0) + processed.get('positive'),
                        'negative' : processed_data_value.get('negative', 0) + processed.get('negative'),
                        'neutral' : processed_data_value.get('neutral', 0) + processed.get('neutral')
                    }
                })
            else:
                self.processed_data[search_term] = {
                    'positive' : processed.get('positive'),
                    'negative' : processed.get('negative'),
                    'neutral' : processed.get('neutral')
                }

    def flush_processed_data(self):
        print('Flushing data...')
        for key in self.processed_data:
            value = self.processed_data.get(key)
            dashboard_id = self.terms_dict.get(key).get('id')
            user_id = self.terms_dict.get(key).get('user_id')
            report_period = ReportPeriod()
            report_period.start = self.period_start
            report_period.end = int(time.time())
            report_period.positive = value.get('positive')
            report_period.negative = value.get('negative')
            report_period.neutral = value.get('neutral')
            self.db.add_period_data(user_id, dashboard_id, report_period)
        self.processed_data = {}
        self.schedule_next_data_flush()
    
    def schedule_next_data_flush(self):
        self.period_start = int(time.time())
        threading.Timer(self.REPORT_PERIOD_DURATION, self.flush_processed_data).start()
