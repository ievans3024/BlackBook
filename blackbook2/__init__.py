__author__ = 'ievans3024'


import flask_whooshalchemy as whooshalchemy

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import Person


app = Flask(__name__)

app.config.from_pyfile('config.cfg', silent=True)

db = SQLAlchemy(app)


@app.route('/')
@app.route('/book')
def home():
    """Home Page, displays references to all entries"""
    return render_template('base.html')


@app.route('/api/')
def api():
    pass


@app.route('/api/doc/')
def api_doc():
    return render_template('api.html')


@app.route('/api/entry/', methods=['GET', 'POST'])
@app.route('/api/entry/<int:person_id>/', methods=['GET', 'DELETE', 'PATCH'])
def api_entry(person_id=None):
    pass


@app.route('/api/search/')
def api_search():
    # TODO: requires python 2 until Flask-WhooshAlchemy supports python 3
    pass


if __name__ == '__main__':
    whooshalchemy.whoosh_index(app, Person)  # TODO: figure out if this should be a cron job instead
    app.run()