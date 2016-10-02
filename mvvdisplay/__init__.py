from flask import Flask

app = Flask(__name__)

DEBUG = False

app.config.from_object(__name__)
