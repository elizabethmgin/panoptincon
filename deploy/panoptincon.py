from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy
from  models import SMS, User, Status


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['MONGOALCHEMY_DATABASE'] = 'smsTest2'
db = MongoAlchemy(app)

import views
import utilities

if __name__ == "__main__":
    app.run()
