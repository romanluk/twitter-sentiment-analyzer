class User(object):
    def __init__(self, uid):
        self.uid = uid
        self.dashboards = []

class Dashboard(object):
    def __init__(self):
        self.title = ""
        self.search_term = ""
        self.periods = []

    @staticmethod
    def from_dict(src):
        dashboard = Dashboard()
        dashboard.title = src.get('title')
        dashboard.search_term = src.get('search_term')
        dashboard.periods = src.get('periods')
        return dashboard

class ReportPeriod(object):
    def __init__(self):
        self.start = 0
        self.end = 0