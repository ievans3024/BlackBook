import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from blackbook.api import ContactAPI, SessionAPI, UserAPI

__author__ = 'ievans3024'


def load_config_from_env():
    config = {}
    for k in app.config.keys():
        try:
            config[k] = os.environ[k]
        except KeyError:
            pass
    return config

app = Flask('blackbook')

app.config.setdefault('BLACKBOOK_PASSWORD_HASH_METHOD', 'pbkdf2:sha512')
app.config.setdefault('BLACKBOOK_PASSWORD_SALT_LENGTH', 12)
app.config.setdefault('BLACKBOOK_API_URL_ROOT', '/api/')
app.config.setdefault('BLACKBOOK_API_PAGINATION_PER_PAGE', 10)

app.config.from_pyfile('config.py', silent=True)
env_config = load_config_from_env()
app.config.update(**env_config)

app.db = SQLAlchemy(app)

api_root = app.config.get('BLACKBOOK_API_URL_ROOT')

app.add_url_rule(api_root + 'contact/', view_func=ContactAPI.as_view('contacts', app, app.db, api_root + 'contact/'))
app.add_url_rule(api_root + 'contact/<contact_id>/',
                 view_func=ContactAPI.as_view('contact', app, app.db, api_root + 'contact/'))
app.add_url_rule(api_root + 'session/', view_func=SessionAPI.as_view('sessions', app, app.db, api_root + 'session/'))
app.add_url_rule(api_root + 'user/', view_func=UserAPI.as_view('users', app, app.db, api_root + 'user/'))
app.add_url_rule(api_root + 'user/<user_id>/', view_func=UserAPI.as_view('user', app, app.db, api_root + 'user/'))


@app.route("/")
def home():
    return render_template("base.html")

if __name__ == "__main__":
    app.run()
