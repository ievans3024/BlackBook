from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

__author__ = 'ievans3024'

app = Flask('blackbook')
app.config.from_pyfile('config.py', silent=True)
app.db = SQLAlchemy(app)

# Must occur after app has been created and db has been registered
from .api import collectionplusjson, html, json, xml


@app.route("/")
@app.route("/book/")
def home():
    return render_template("base.html")

if __name__ == "__main__":
    app.run()
