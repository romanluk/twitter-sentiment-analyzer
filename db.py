import firebase_admin, entities
from firebase_admin import credentials, firestore
from entities import User, Dashboard, ReportPeriod

class FirestoreDb(object):
    __instance = None

    @staticmethod
    def get_instance():
        if FirestoreDb.__instance == None:
            FirestoreDb()
        return FirestoreDb.__instance        

    def __init__(self):
        if FirestoreDb.__instance != None:
            raise Exception("FirestoreDb::constructor called on singleton class")
        else:
            cred = credentials.Certificate('./service_account_key.json')
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            print("Firestore DB class initialized")
            FirestoreDb.__instance = self

    def add_user(self, uid):
        self.db.collection(u'users').document(uid).set({})

    def add_dashboard(self, user_id, dashboard):
        dashboards_ref = self.db.collection(u'users').document(user_id).collection(u'dashboards')
        dashboards_ref.add({
            u'title' : dashboard.title,
            u'search_term' : dashboard.search_term
        })
    
    def add_period_data(self, user_id, dashboard_id, period_data):
        dashboards_ref = self.db.collection(u'users').document(user_id).collection(u'dashboards')
        dashboards_ref.document(dashboard_id).collection('periods').add({
            u'start' : period_data.start,
            u'end' : period_data.end
        })

    def get_dashboards(self, user_id):
        dashboards = self.db.collection(u'users').document(user_id).collection(u'dashboards').get()
        return [Dashboard.from_dict(dashboard.to_dict()) for dashboard in dashboards]