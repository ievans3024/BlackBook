from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from blackbook.api import ContactAPI, SessionAPI, UserAPI

__author__ = 'ievans3024'

app = Flask('blackbook')
app.config.from_pyfile('config.py', silent=True)
app.db = SQLAlchemy(app)

app.add_url_rule('/api/contact/', view_func=ContactAPI.as_view('contacts', app, app.db, '/api/contact/'))
app.add_url_rule('/api/contact/<contact_id>/', view_func=ContactAPI.as_view('contact', app, app.db, '/api/contact/'))
app.add_url_rule('/api/session/', view_func=SessionAPI.as_view('sessions', app, app.db, '/api/session/'))
app.add_url_rule('/api/user/', view_func=UserAPI.as_view('users', app, app.db, '/api/user/'))
app.add_url_rule('/api/user/<user_id>/', view_func=UserAPI.as_view('user', app, app.db, '/api/user/'))


@app.route("/")
def home():
    return render_template("base.html")

if __name__ == "__main__":
    app.run()
