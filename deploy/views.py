"""
views.py

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
import models
from utilities import showlocation, showtime, showtimeandloc, calcTime
from HTMLParser import HTMLParser
from models import User, SMS, Status

from panoptincon import app
#app.config.from_object('config')
#app.config.from_pyfile('config.py')
db = MongoAlchemy(app)

MASTER_NUMBER = '16262190621'

#we need to set up our own config files
auth_id = app.config['AUTH_ID']
auth_token = app.config['AUTH_TOKEN']

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

@app.route("/")
def welcome():
    return "this is a test"
    
    
@app.route("/plivo/sms/", methods=['GET', 'POST'])
def sms():
    if request.method == 'POST':
        print >> sys.stderr, "Received POST request to /plivo/sms/" # this is how you write messages to yourself in the Apache /var/log/apache2/error.log
        try:
	    s = 'in the try'
            print >> sys.stderr, s
            s = SMS(timeAnswered = datetime.datetime.now(),
                                action = 'super text',
                                direction = 'incoming',
                                smsTo = request.form['To'],
                                smsType = request.form['Type'],
                                smsMessageUUID = request.form['MessageUUID'],
                                smsFrom = request.form['From'],
                                smsText = request.form['Text'],
                                )
            print >> sys.stderr, s.direction
            s.save()
            message = request.form['Text']
            caller = request.form['From']
            regisUser = User.query.filter(User.number == caller).first()
            newMessage = showlocation(message)
            print >> sys.stderr, newMessage
            send_txt(caller,newMessage.upper())
        except:
            print >> sys.stderr, str(sys.exc_info()[0])
            print >> sys.stderr, str(sys.exc_info()[1])
            #entering the gateway where stuff happens!
    else:
        return "These aren't the droids you're looking for. Move along, move along."
        
@app.route("/cron")
def cron():
    users = User.query.all()
    for u in users:
        if u.status.timeExpired == datetime.datetime.now():
            send_txt(u.number, "Are you alright?", src=MASTER_NUMBER)
    return "cron done run."
   
def send_txt(destination, text, src='16262190621'):
    p = plivo.RestAPI(auth_id, auth_token) # Create a Plivo API object, used when you want to write to their service
    params = { 'text':text,
              'src':src,
              'dst':destination,
              }
    p.send_message(params) # A method in the object for sending sms

if __name__ == '__main__':
    app.run(debug=True)
