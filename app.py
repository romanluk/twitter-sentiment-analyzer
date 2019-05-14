from flask import Flask, abort, request, jsonify
import csv
import sys
import os
from  twitter_sentiment_analyzer.TwitterClient import TwitterClient, TwitterStreamListener
from db import FirestoreDb

app = Flask(__name__)

@app.route('/search-terms', methods=['GET', 'POST'])
def searchTerms():
    if request.method == 'POST':
        if not os.path.exists('data'):
            os.makedirs('data')
        with open('data/terms.csv', 'a+') as terms_file:
            terms_writer = csv.writer(terms_file, delimiter=',')
            userId = request.form.get('userId')
            term = request.form.get('term')
            terms_writer.writerow([userId, term])
            return jsonify(success = True, message = 'Success', data = term), 200
    elif request.method == 'GET':
        pass

@app.route('/dashboards', methods=['GET'])
def dashboards():
    user_id = request.args.get('user_id')
    if user_id:
        db = FirestoreDb.get_instance()
        dashboards = db.get_dashboards(user_id)
        return jsonify(success = True, data = [dashboard.serialize() for dashboard in dashboards])
    else:
        return jsonify(success = False, Message = "Missing mandatory parameter user_id")

def setup():
    prepareTwitterClient()
    app.run(debug = True)

def prepareTwitterClient():
    twitter_client = TwitterClient(TwitterStreamListener())
    twitter_client.filter(['Donald'])
setup()