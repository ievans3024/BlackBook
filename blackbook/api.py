__author__ = 'ievans3024'

"""
AJAX API routes
"""

from blackbook import app, db, render_template, request_accepts, request
from blackbook.collection import MIMETYPE as CPJSON
from collection_json import Collection, Link
from flask import abort, json, Response

API_ROOT = app.config.get('API_ROOT')


@app.route('/api/')
def api():
    if not request_accepts(CPJSON):
        abort(406)
    response = Collection(API_ROOT)
    response.links.append(Link('/api/entry/', 'index', prompt='List all entries or add an entry'))
    return Response(json.dumps(response.to_dict()), mimetype=CPJSON)


@app.route('/api/doc/')
def api_doc():
    return render_template('api.html')


@app.route('/api/entry/', methods=['GET', 'POST'])
def api_entries():
    if not request_accepts(CPJSON):
        abort(406)
    if request.method == 'GET':
        # return paginated contact info
        response = db.read(
            page=request.args.get('page') or 1,
            per_page=request.args.get('per_page') or 5
        )
        return Response(json.dumps(response.to_dict()), mimetype=CPJSON)
    else:
        if request.mimetype != CPJSON:
            abort(415)
        # TODO: Form validation
        try:
            created_entry = db.create(json.loads(request.data.decode()))
        except (TypeError, ValueError) as e:
            # TODO: Create custom error classes in database code, raise those instead.
            abort(400)
        return Response(json.dumps(created_entry.to_dict()), mimetype=CPJSON), 201


@app.route('/api/entry/<int:person_id>/', methods=['GET', 'DELETE', 'PATCH'])
def api_entry(person_id=None):
    if isinstance(person_id, int):
        if not request_accepts(CPJSON):
            abort(406)
        else:
            if request.method == 'GET':
                # return person info
                response = db.read(
                    id=person_id,
                    page=request.args.get('page') or 1,
                    per_page=request.args.get('per_page') or 5
                )
                return Response(json.dumps(response.to_dict()), mimetype=CPJSON)
            elif request.method == 'DELETE':
                # process contact deletion request
                try:
                    deleted = db.delete(person_id)
                except Exception as e:
                    raise e
                else:
                    if not deleted:
                        return '', 204
                    else:
                        return Response(
                            json.dumps(deleted.to_dict()), mimetype=CPJSON
                        ), int(deleted.error.code)
            else:
                if request.mimetype != CPJSON:
                    abort(415)
                pass  # assume PATCH? process contact modification request
    else:
        abort(404)


@app.route('/api/search/')
def api_search():
    # Coming soon!
    abort(501)

if app.config.get('TESTING'):
    @app.route('/tests/')
    def tests():
        """
        Front-to-back api unittests
        """
        return render_template('tests.html')