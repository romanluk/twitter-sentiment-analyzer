class User(object):
    def __init__(self, uid):
        self.uid = uid
        self.dashboards = []

class Dashboard(object):
    def __init__(self):
        self.title = ""
        self.search_term = ""
        self.periods = []

class ReportPeriod(object):
    def __init__(self):
        self.start = 0
        self.end = 0