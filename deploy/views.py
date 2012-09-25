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
from utilities import check_in_parsing, listserve_broadcast, group_maintenance, help_parsing, check_time
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

commands = {'@':check_in_parsing,
            '!':listserve_broadcast,
            'g':group_maintenance,
            'h':help_parsing,
            }

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
            #response = showtimeandloc(message)
            #Dispatcher for the various commands
            try:
                response = commands[message[0]](message)
            except:
                response = "This was not a valid command.  Try @,!,g, or h.  H for help."

            print >> sys.stderr, response
            caller = request.form['From']
            if User.query.filter(User.number == caller).first():
                if type(response) == type(dict()):
                    regisUser = User.query.filter(User.number == caller).first()
                    location = response['location']
                    print >> sys.stderr, location
                    hours = int(response['hours'])
                    print >> sys.stderr, hours
                    timeExpired = datetime.datetime.now() + datetime.timedelta(hours=hours)
                    print >> sys.stderr, timeExpired
                    condition = 'safe'
                    newStatus = Status(location=location,timeEntered=datetime.datetime.now(),timeExpired=timeExpired,condition=condition)
                    newStatus.save()
                    regisUser.status = newStatus
                    regisUser.save()
                    yourStatus = 'We know you are at ' + location + ' for ' + str(hours) + ' hours. Now we are watching you.'
                    send_txt(caller,yourStatus.upper())
                elif type(response) == type(str()):
                    send_txt(caller,response.upper(), src=MASTER_NUMBER)
                else:
                    oops = 'Sorry. We are confused. Please try again.'
                    send_txt(caller,oops.upper())
            else:
                response = "Welcome to Panoptincon, where we aren't always watching. Your default location is Speke Apartments."
                timeExpired = datetime.datetime.now() + datetime.timedelta(hours=24)
                newStatus = Status(location='Speke Apartments',timeEntered=datetime.datetime.now(),timeExpired=timeExpired,condition='safe')
                newStatus.save()
                newUser = User(number=caller, status=newStatus, createdAt=datetime.datetime.now(), name=message, isChin=False)
                newUser.save()
                send_txt(caller,response.upper(), src=MASTER_NUMBER)
        except:
            print >> sys.stderr, str(sys.exc_info()[0])
            print >> sys.stderr, str(sys.exc_info()[1])
            #entering the gateway where stuff happens!
    else:
        return "These aren't the droids you're looking for. Move along, move along."
        
@app.route("/cron")
def cron():
    check_time()
    return "cron done run."
   
def send_txt(destination, text, src=MASTER_NUMBER):
    p = plivo.RestAPI(auth_id, auth_token) # Create a Plivo API object, used when you want to write to their service
    params = { 'text':text,
              'src':src,
              'dst':destination,
              }
    p.send_message(params) # A method in the object for sending sms

if __name__ == '__main__':
    app.run(debug=True)
