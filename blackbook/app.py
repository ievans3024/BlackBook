__author__ = 'ievans3024'

from flask import Flask, render_template
from importlib import import_module

app = Flask('blackbook')
app.config.from_pyfile('config.py', silent=True)

try:
    plugin = import_module(app.config.get("DATABASE_HANDLER"))
    print(dir(plugin))
except AttributeError:
    raise ValueError("Config option 'DATABASE_HANDLER' is an invalid value or does not exist.")
except ImportError:
    raise ValueError(
        "Config option 'DATABASE_HANDLER' is {value} but there is no such module".format(
            value=app.config.get("DATABASE_HANDLER")
        )
    )
except SystemError:
    raise ValueError(
        "Config option 'DATABASE_HANDLER' "
    )
except ValueError:
    raise ValueError("Config option 'DATABASE_HANDLER' cannot be empty.")
else:
    app.register_blueprint(plugin.api_blueprint)

@app.route("/")
@app.route("/book/")
def home():
    return render_template("base.html")

if __name__ == "__main__":
    app.run()