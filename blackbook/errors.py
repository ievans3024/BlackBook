__author__ = 'ievans3024'

from blackbook import app, request_accepts
from blackbook.collection import MIMETYPE as CPJSON
from collection_json import Error
from flask import json, render_template
from os.path import join


@app.errorhandler(400)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(406)
@app.errorhandler(415)
def generic_error(e):
    if request_accepts(CPJSON):
        error = Error(code=e.code, message=e.description, title=e.name)
    elif request_accepts('application/json'):
        error = json.dumps(
            {
                'code': e.code,
                'message': e.description,
                'title': e.name
            }
        )
    else:
        error = render_template(join('errors', 'base_error.html'), error=e)
    return error, e.code