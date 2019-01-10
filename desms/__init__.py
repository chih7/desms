import configparser
import logging

# Load data from config.ini file
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

config = configparser.ConfigParser()
config.read('config/config.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config['TELEGRAM']['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

# Initial db
db = SQLAlchemy(app)

app.config.from_object(__name__)

#create all db tables
@app.before_first_request
def create_tables():
    from desms.models import SMSForm
    db.create_all()

from desms import main
