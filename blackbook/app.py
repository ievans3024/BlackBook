__author__ = 'ievans3024'

from flask import Flask, render_template
from importlib import import_module

app = Flask('blackbook')
app.config.from_pyfile('config.py', silent=True)

try:
    plugin = import_module(app.config.get("DATABASE_PLUGIN"))
except AttributeError:
    raise ValueError("Config option 'DATABASE_PLUGIN' is an invalid value or does not exist.")
except ImportError:
    raise ValueError(
        "Config option 'DATABASE_PLUGIN' is {value} but there is no such module".format(
            value=app.config.get("DATABASE_PLUGIN")
        )
    )
except SystemError:
    raise ValueError(
        "Module referenced by config option 'DATABASE_PLUGIN' cannot be imported."
    )
except ValueError:
    raise ValueError("Config option 'DATABASE_PLUGIN' cannot be empty.")
else:
    api = plugin.api.init_api(app)
    app.register_blueprint(api)

@app.route("/")
@app.route("/book/")
def home():
    return render_template("base.html")

if __name__ == "__main__":
    app.run()