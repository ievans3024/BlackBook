from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from blackbook.api import ContactAPI, SessionAPI, UserAPI
from datetime import timedelta

__author__ = 'ievans3024'

app = Flask('blackbook')

app.config.setdefault('PERMANENT_SESSION_LIFETIME', timedelta(days=14))
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
app.config.setdefault('PASSWORD_HASH_METHOD', 'pbkdf2:sha512')
app.config.setdefault('PASSWORD_SALT_LENGTH', 12)
app.config.setdefault('API_URL_ROOT', '/api/')
app.config.setdefault('API_PAGINATION_PER_PAGE', 10)

app.config.from_pyfile('config.py', silent=True)

app.db = SQLAlchemy(app)

app.add_url_rule(app.config.get('API_URL_ROOT') + 'contact/',
                 view_func=ContactAPI.as_view('contacts', app, app.db, '/api/contact/'))
app.add_url_rule(app.config.get('API_URL_ROOT') + 'contact/<contact_id>/',
                 view_func=ContactAPI.as_view('contact', app, app.db, '/api/contact/'))
app.add_url_rule(app.config.get('API_URL_ROOT') + 'session/',
                 view_func=SessionAPI.as_view('sessions', app, app.db, '/api/session/'))
app.add_url_rule(app.config.get('API_URL_ROOT') + 'user/',
                 view_func=UserAPI.as_view('users', app, app.db, '/api/user/'))
app.add_url_rule(app.config.get('API_URL_ROOT') + 'user/<user_id>/',
                 view_func=UserAPI.as_view('user', app, app.db, '/api/user/'))


@app.route("/")
def home():
    return render_template("base.html")

if __name__ == "__main__":
    app.run()
