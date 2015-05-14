__author__ = 'ievans3024'

from flask import Flask, render_template

app = Flask('blackbook')
app.config.from_pyfile('config.py', silent=True)


@app.route("/")
@app.route("/book/")
def home():
    return render_template("base.html")

if __name__ == "__main__":
    app.run()