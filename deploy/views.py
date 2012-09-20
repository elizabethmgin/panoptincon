"""
Created by Media Design Practices: Field at Art Center College of Design.
Copyright (c) 2012 MDP. All rights reserved.
Licensed under the Affero 3 GPL License
http://www.gnu.org/licenses/agpl.txt

"""

import datetime
from flask import Flask
from flask import request, url_for, render_template
from flaskext.mongoalchemy import MongoAlchemy
import feedparser
import plivo
import sys
import re
from HTMLParser import HTMLParser
app = Flask(__name__)
app.config.from_object('config')
app.config['MONGOALCHEMY_DATABASE'] = 'smsTest'
db = MongoAlchemy(app)

#we need to set up our own config files
auth_id = app.config('AUTH_ID')
auth_token = app.config('AUTH_TOKEN')

#are you going to use a database? if so, what classes do we need?
class SMS(db.Document):
    timeAnswered = db.DateTimeField()
    action = db.StringField()
    direction = db.StringField()
    smsTo = db.StringField()
    smsType = db.StringField()
    smsMessageUUID = db.StringField()
    smsFrom = db.StringField()
    smsText = db.StringField()

#what other information do we need to store about each user?
class User(db.Document):
    number = db.ListField(db.StringField())
    status = db.StringField()
    createdAt = db.DateTimeField(required=True)
    name = db.StringField()
    
class Event(db.Document):
    

#this HTMLParser is good for cleaning up input from web forms if we choose to have a web component
#we should review it though and possibly add to it based on our needs    
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self,d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
    
@app.route("/plivo/sms/", methods=['GET', 'POST'])
def sms():
    if request.method == 'POST':
        print >> sys.stderr, "Received POST request to /plivo/sms/" # this is how you write messages to yourself in the Apache /var/log/apache2/error.log
        try:
            #entering the gateway where stuff happens!
    else:
        return "These aren't the droids you're looking for. Move along, move along."
        
def send_txt(destination, text, src='16262190621'):
    p = plivo.RestAPI(auth_id, auth_token) # Create a Plivo API object, used when you want to write to their service
    params = { 'text':text,
              'src':src,
              'dst':destination,
              }
    p.send_message(params) # A method in the object for sending sms

if __name__ == '__main__':
    app.run(debug=True)