import time, threading
from db import FirestoreDb
from entities import ReportPeriod
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
            self.REPORT_PERIOD_DURATION = 5 #seconds
            self.period_start = 0
            self.tracks = []
            self.terms_dict = {}
            self.precessed_data = {}
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
        self.twitter_stram_listener.terminate()
        self.twitter_client.filter(self.tracks)

    def start(self):
        self.update_twitter_client_tracks()
        self.schedule_next_data_flush()
    
    def on_data_callback(self, data):
        processed = {
            'search_term' : 'kk',
            'positive' : 3,
            'negative' : 2,
            'neutral' : 1
        }
        self.precessed_data.update({
            processed.get('search_term') : {
                'positive' : self.precessed_data.get('positive', 0) + processed.get('positive'),
                'negative' : self.precessed_data.get('negative', 0) + processed.get('negative'),
                'neutral' : self.precessed_data.get('neutral', 0) + processed.get('neutral')
            }
        })

    def flush_processed_data(self):
        print('Flushing data...')
        for key in self.precessed_data:
            value = self.precessed_data.get(key)
            dashboard_id = self.terms_dict.get(key).get('id')
            user_id = self.terms_dict.get(key).get('user_id')
            report_period = ReportPeriod()
            report_period.start = self.period_start
            report_period.end = int(time.time())
            report_period.positive = value.get('positive')
            report_period.negative = value.get('negative')
            report_period.neutral = value.get('neutral')
            self.db.add_period_data(user_id, dashboard_id, report_period)
        self.schedule_next_data_flush()
    
    def schedule_next_data_flush(self):
        self.period_start = int(time.time())
        threading.Timer(self.REPORT_PERIOD_DURATION, self.flush_processed_data).start()
