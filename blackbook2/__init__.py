__author__ = 'ievans3024'


import flask_whooshalchemy as whooshalchemy

from collection import CollectionPlusJSON, COLLECTION_JSON
from flask import Flask, render_template, request, abort, Response


app = Flask(__name__)

app.config.from_pyfile('config.cfg', silent=True)

# this import needs db to exist first
from models import Person, generate_test_db


def new_entry():
    """Creates a new Person"""
    pass


def edit_entry(person_id):
    """Edits Person by id"""
    pass


def delete_entry(person_id):
    """Deletes person by id"""
    pass


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
@app.route('/api/entry/<int:person_id>/', methods=['GET', 'DELETE', 'PATCH'])
def api_entry(person_id=None):
    if person_id is None:
        if request.method == 'GET':
            if not request_accepts(COLLECTION_JSON):
                abort(406)
            # return paginated contact info
            response_object = CollectionPlusJSON()
            # TODO: Paginate query
            # TODO: Trim listing down to more basic info, fetch details on individual entry
            for person in Person.query.all():
                response_object.append_item(person.get_collection_object())
            return Response(str(response_object), mimetype=COLLECTION_JSON)
        else:
            if request.mimetype != COLLECTION_JSON:
                abort(415)
            pass  # assume POST? process new contact creation request
    else:
        if request.method == 'GET':
            if not request_accepts(COLLECTION_JSON):
                abort(406)
            pass  # return person info
        elif request.method == 'DELETE':
            pass  # process contact deletion request
        else:
            if request.mimetype != COLLECTION_JSON:
                abort(415)
            pass  # assume PATCH? process contact modification request


@app.route('/api/search/')
def api_search():
    # TODO: requires python 2 until Flask-WhooshAlchemy supports python 3
    pass


if __name__ == '__main__':
    # generate_test_db()  # uncomment to generate test database
    whooshalchemy.whoosh_index(app, Person)  # TODO: figure out if this should be a scheduled task instead
    app.run()