__author__ = 'ievans3024'

import flask_whooshalchemy as whooshalchemy
from collection import CollectionPlusJSON, COLLECTION_JSON
from flask import Flask, render_template, request, abort, Response


# TODO: Learn how to use global object (g)

app = Flask(__name__)

app.config.from_pyfile('config.py', silent=True)

# this import needs db to exist first
if app.config.get('DATABASE_HANDLER') in ('sqlite', 'mysql', 'postgresql'):
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
    response_data = CollectionPlusJSON()
    response_data.append_link('/api/entry/', 'index', 'List all entries or add an entry')
    return Response(str(response_data), mimetype=COLLECTION_JSON)


@app.route('/api/doc/')
def api_doc():
    return render_template('api.html')


@app.route('/api/entry/', methods=['GET', 'POST'])
def api_entries():
    api_href = '/api/entry/'
    if not request_accepts(COLLECTION_JSON):
        abort(406)
    if request.method == 'GET':
        # return paginated contact info
        response_object = db.read(
            page=request.args.get('page') or 1,
            per_page=request.args.get('per_page') or 5,
            endpoint_uri=api_href
        )
        return Response(str(response_object), mimetype=response_object.mimetype)
    else:
        if request.mimetype != COLLECTION_JSON:
            abort(415)
        try:
            # TODO: Form validation
            created_entry = db.create(request.data)
        except Exception as e:
            raise e
        else:
            return Response(str(created_entry), mimetype=created_entry.mimetype), 201


@app.route('/api/entry/<int:person_id>/', methods=['GET', 'DELETE', 'PATCH'])
def api_entry(person_id=None):
    if isinstance(person_id, int):
        api_href = '/api/entry/%d' % person_id
        if not request_accepts(COLLECTION_JSON):
            abort(406)
        else:
            if request.method == 'GET':
                # return person info
                response_object = db.read(
                    id=person_id,
                    page=request.args.get('page') or 1,
                    per_page=request.args.get('per_page') or 5,
                    endpoint_uri=api_href
                )
                return Response(str(response_object), mimetype=response_object.mimetype)
            elif request.method == 'DELETE':
                # process contact deletion request
                try:
                    db.delete(person_id)
                except Exception as e:
                    raise e
                else:
                    return '', 204
            else:
                if request.mimetype != COLLECTION_JSON:
                    abort(415)
                pass  # assume PATCH? process contact modification request
    else:
        abort(404)


@app.route('/api/search/')
def api_search():
    pass


if __name__ == '__main__':
    # db.generate_test_db()  # uncomment to generate test database
    # whooshalchemy.whoosh_index(app, Person)  # TODO: figure out if this should be a scheduled task instead
    app.run()