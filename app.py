from flask import Flask, abort, request, jsonify
import csv
import sys
import os
from  twitter_sentiment_analyzer.TwitterClient import TwitterClient, TwitterStreamListener
from db import FirestoreDb
from entities import Dashboard

app = Flask(__name__)

@app.route('/dashboards', methods=['GET', 'POST'])
def dashboards():
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        if user_id:
            db = FirestoreDb.get_instance()
            dashboards = db.get_dashboards_for_user(user_id)
            return jsonify(success = True, data = [dashboard.serialize() for dashboard in dashboards])
        else:
            return jsonify(success = False, Message = "Missing mandatory parameter user_id")
    elif request.method == 'POST':
        payload = request.get_json()
        user_id = payload.get('user_id')
        title = payload.get('title')
        search_term = payload.get('search_term')
        if user_id and title and search_term:
            db = FirestoreDb.get_instance()
            dashboard = Dashboard()
            dashboard.title = title
            dashboard.search_term = search_term
            db.add_dashboard(user_id, dashboard)
            return jsonify(success = True)
        else:
            return jsonify(success = False, Message = "Missing mandatory parameter (e.g. user_id/title/search_term)")


def setup():
    # prepareTwitterClient()
    app.run(debug = True)

def prepareTwitterClient():
    twitter_client = TwitterClient(TwitterStreamListener())
    twitter_client.filter(['Donald'])
setup()