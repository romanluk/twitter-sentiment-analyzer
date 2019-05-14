class User(object):
    def __init__(self, uid):
        self.uid = uid
        self.dashboards = []

class Dashboard(object):
    def __init__(self):
        self.id = ""
        self.title = ""
        self.search_term = ""
        self.periods = []

    @staticmethod
    def from_dict(src):
        dashboard = Dashboard()
        dashboard.id = src.get('id')
        dashboard.title = src.get('title')
        dashboard.search_term = src.get('search_term')
        dashboard.periods = src.get('periods')
        return dashboard

    def serialize(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'search_term' : self.search_term,
            'periods' : [period.serialize() for period in self.periods] if self.periods != None else []
        }

class ReportPeriod(object):
    def __init__(self):
        self.start = 0
        self.end = 0

    def serialize(self):
        return {
            'start' : self.start,
            'end' : self.end
        }