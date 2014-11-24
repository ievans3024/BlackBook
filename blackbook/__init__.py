__author__ = 'ievans3024'

#import flask_whooshalchemy as whooshalchemy
import json
from collection_json import Collection, Link
from flask import Flask, render_template, request, abort, Response


# TODO: Learn how to use global object (g)
COLLECTION_JSON = 'application/vnd.collection+json'

app = Flask(__name__)

app.config.from_pyfile('config.py', silent=True)

# this import needs db to exist first
if (not app.config.get('DATABASE_HANDLER')) or (app.config.get('DATABASE_HANDLER') == 'flatfile'):
    from blackbook.database.flatdatabase import FlatDatabase
    db = FlatDatabase(app)
elif app.config.get('DATABASE_HANDLER') in ('sqlite', 'mysql', 'postgresql'):
    from blackbook.database.sqlalchemy import SQLAlchemyDatabase
    db = SQLAlchemyDatabase(app)


def request_accepts(*mimetypes):
    best = request.accept_mimetypes.best_match(mimetypes)
    return request.accept_mimetypes[best] and request.accept_mimetypes[best] >= request.accept_mimetypes['text/html']


@app.route('/')
@app.route('/book/')
def home():
    """Home Page, displays references to all entries"""
    return render_template('base.html')


@app.route('/api/')
def api():
    if not request_accepts(COLLECTION_JSON):
        abort(406)
    response = Collection('/api/')
    response.links.append(Link('/api/entry/', 'index', prompt='List all entries or add an entry'))
    return Response(json.dumps(response.to_dict()), mimetype=COLLECTION_JSON)


@app.route('/api/doc/')
def api_doc():
    return render_template('api.html')


@app.route('/api/entry/', methods=['GET', 'POST'])
def api_entries():
    if not request_accepts(COLLECTION_JSON):
        abort(406)
    if request.method == 'GET':
        # return paginated contact info
        response = db.read(
            page=request.args.get('page') or 1,
            per_page=request.args.get('per_page') or 5
        )
        return Response(json.dumps(response.to_dict()), mimetype=COLLECTION_JSON)
    else:
        if request.mimetype != COLLECTION_JSON:
            abort(415)
        # TODO: Form validation
        try:
            created_entry = db.create(json.loads(request.data.decode()))
        except (TypeError, ValueError) as e:
            # TODO: Create custom error classes in database code, raise those instead.
            abort(400)
        return Response(json.dumps(created_entry.to_dict()), mimetype=COLLECTION_JSON), 201


@app.route('/api/entry/<int:person_id>/', methods=['GET', 'DELETE', 'PATCH'])
def api_entry(person_id=None):
    if isinstance(person_id, int):
        if not request_accepts(COLLECTION_JSON):
            abort(406)
        else:
            if request.method == 'GET':
                # return person info
                response = db.read(
                    id=person_id,
                    page=request.args.get('page') or 1,
                    per_page=request.args.get('per_page') or 5
                )
                return Response(json.dumps(response.to_dict()), mimetype=COLLECTION_JSON)
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
                            json.dumps(deleted.to_dict()), mimetype=COLLECTION_JSON
                        ), int(deleted.error.code)
            else:
                if request.mimetype != COLLECTION_JSON:
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


if __name__ == '__main__':
    try:
        db.generate_test_db()  # uncomment to generate test database
    except IndexError:
        pass
    # whooshalchemy.whoosh_index(app, Person)  # TODO: figure out if this should be a scheduled task instead
    app.run()