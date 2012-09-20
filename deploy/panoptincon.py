from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy
from  models import SMS, User, Status
import utilities
#import views

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['MONGOALCHEMY_DATABASE'] = 'smsTest'
db = MongoAlchemy(app)

import views

if __name__ == "__main__":
    app.run()
