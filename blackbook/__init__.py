__author__ = 'ievans3024'

# FIXME: Move this out of __init__ to prevent accidental double imports

#import flask_whooshalchemy as whooshalchemy

from flask import Flask, request, render_template

# TODO: Learn how to use global object (g)
# TODO: Add errors module with generic error handler, use abort() accordingly

app = Flask(__name__)

app.config.from_pyfile('config.py', silent=True)

# this import needs app to exist first
from blackbook.database import db


def request_accepts(*mimetypes):
    best = request.accept_mimetypes.best_match(mimetypes)
    return request.accept_mimetypes[best] and request.accept_mimetypes[best] >= request.accept_mimetypes['text/html']


@app.route('/')
@app.route('/book/')
def home():
    """Home Page, displays references to all entries"""
    return render_template('base.html')

# Have to re-import app after adding routes, errors, etc.
from blackbook.errors import app
from blackbook.api import app

if __name__ == '__main__':
    try:
        db.generate_test_db()  # uncomment to generate test database
    except IndexError:
        pass
    # whooshalchemy.whoosh_index(app, Person)  # TODO: figure out if this should be a scheduled task instead
    app.run()