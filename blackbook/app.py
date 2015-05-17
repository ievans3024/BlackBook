__author__ = 'ievans3024'

from flask import Flask, render_template
from importlib import import_module

app = Flask('blackbook')
app.config.from_pyfile('config.py', silent=True)

try:
    plugin = import_module(app.config.get("DATABASE_HANDLER"))
except AttributeError:
    raise ValueError("Config option 'DATABASE_HANDLER' is an invalid value or does not exist.")
except ValueError:
    raise ValueError("Config option 'DATABASE_HANDLER' cannot be empty.")
except ImportError:
    raise ValueError("Config option 'DATABASE_HANDLER' is {value} but there is no module to support that".format(value=app.config.get("DATABASE_HANDLER")))

app.register_blueprint(plugin.api)

@app.route("/")
@app.route("/book/")
def home():
    return render_template("base.html")

if __name__ == "__main__":
    app.run()