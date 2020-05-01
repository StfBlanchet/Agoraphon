from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

from app import main
