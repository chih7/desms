import configparser
import logging

# Enable logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

config = configparser.ConfigParser()
config.read('config/config.ini')

TOKEN = config['TELEGRAM']['ACCESS_TOKEN']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = TOKEN
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

# Initial db
db = SQLAlchemy(app)
