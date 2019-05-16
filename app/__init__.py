from flask import Flask
from app.settings import config
import os


app = Flask(__name__)
config_name = os. getenv('FLASK_CONFIG', 'development')
app.config.from_object(config[config_name])


from app import views, form, model, settings


