from flask import Flask

from app import static
app = Flask(__name__)
app.config.from_object('config')
from app import forms
from app import views
