from flask import Flask, abort, request, jsonify
import csv
import sys
from  twitter_sentiment_analyzer.TwitterClient import TwitterClient, TwitterStreamListener

app = Flask(__name__)

@app.route('/search-terms', methods=['GET', 'POST'])
def searchTerms():
    if request.method == 'POST':
        with open('data/terms.csv', 'a') as terms_file:
            terms_writer = csv.writer(terms_file, delimiter=',')
            term = request.form.get('term')
            terms_writer.writerow([term])
            return jsonify(success = True, message = 'Success', data = term), 200
    elif request.method == 'GET':
        pass


def setup():
    prepareTwitterClient()
    app.run(debug = True)

def prepareTwitterClient():
    twitter_client = TwitterClient(TwitterStreamListener())
    twitter_client.filter(['Donald'])
setup()