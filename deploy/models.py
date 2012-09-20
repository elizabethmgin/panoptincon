"""
models.py

Created by Media Design Practices: Field at Art Center College of Design.
Copyright (c) 2012 MDP. All rights reserved.
Licensed under the Affero 3 GPL License
http://www.gnu.org/licenses/agpl.txt

"""

import datetime
from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy
import plivo

app = Flask(__name__)
app.config.from_object('config')
app.config['MONGOALCHEMY_DATABASE'] = 'smsTest'
db = MongoAlchemy(app)

class SMS(db.Document):
    timeAnswered = db.DateTimeField()
    action = db.StringField()
    direction = db.StringField()
    smsTo = db.StringField()
    smsType = db.StringField()
    smsMessageUUID = db.StringField()
    smsFrom = db.StringField()
    smsText = db.StringField()

class Status(db.Document):
    location = db.StringField()
    timeEntered = db.DateTimeField()
    timeExpired = db.DateTimeField()
    condition = db.StringField()

class User(db.Document):
    number = db.StringField()
    status = db.DocumentField(Status)
    createdAt = db.DateTimeField(required=True)
    name = db.StringField()
    isChin = db.BoolField()
    
