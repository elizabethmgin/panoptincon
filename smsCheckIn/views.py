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

auth_id = app.config('AUTH_ID')
auth_token = app.config('AUTH_TOKEN')