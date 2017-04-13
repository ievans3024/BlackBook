import lib.collection_plus_json as collection_json
import os
from flask import Flask, render_template, request, Response
from api import APIError, ContactAPI, SessionAPI, UserAPI
from database import db

__author__ = 'ievans3024'


app = Flask('blackbook')


def init_api():

    api_root = app.config.get('BLACKBOOK_API_URL_ROOT')

    app.add_url_rule(api_root + 'contact/', view_func=ContactAPI.as_view('contacts', app, db, api_root + 'contact/'))
    app.add_url_rule(api_root + 'contact/<contact_id>/',
                     view_func=ContactAPI.as_view('contact', app, db, api_root + 'contact/'))
    app.add_url_rule(api_root + 'session/', view_func=SessionAPI.as_view('sessions', app, db, api_root + 'session/'))
    app.add_url_rule(api_root + 'user/', view_func=UserAPI.as_view('users', app, db, api_root + 'user/'))
    app.add_url_rule(api_root + 'user/<user_id>/', view_func=UserAPI.as_view('user', app, db, api_root + 'user/'))


def init_config(app):

    app.config.setdefault('BLACKBOOK_PASSWORD_HASH_METHOD', 'pbkdf2:sha512')
    app.config.setdefault('BLACKBOOK_PASSWORD_SALT_LENGTH', 12)
    app.config.setdefault('BLACKBOOK_API_URL_ROOT', '/api/')
    app.config.setdefault('BLACKBOOK_API_PAGINATION_PER_PAGE', 10)

    app.config.from_pyfile('config.py', silent=True)

    # Downside to using os.environ like this is, extraneous
    # vars can leak in, but a good server op can prevent that.
    app.config.update(**os.environ)


@app.errorhandler(APIError)
def handle_api_error(error):
    document = collection_json.Collection(href=error.endpoint)
    document.error = collection_json.Error(code=error.code, title=error.title, message=error.message)
    response = Response(str(document), status=int(error.code), mimetype=document.mimetype)
    return response


@app.route("/")
def home():
    return render_template("base.html")

if __name__ == "__main__":
    init_api()
    app.run()
