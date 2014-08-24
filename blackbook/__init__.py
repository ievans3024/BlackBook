__author__ = 'ievans3024'


import flask_whooshalchemy as whooshalchemy

from collection import CollectionPlusJSON, COLLECTION_JSON
from flask import Flask, render_template, request, abort, Response


app = Flask(__name__)

app.config.from_pyfile('config.cfg', silent=True)

# this import needs db to exist first
from models import Person, generate_test_db, db


def new_entry():
    """Creates a new Person"""
    pass


def edit_entry(person_id):
    """Edits Person by id"""
    pass


def delete_entry(person_id):
    """Deletes person by id"""
    person = Person.query.get_or_404(person_id)

    for email in person.emails:
        db.session.delete(email)
    for phone_number in person.phone_numbers:
        db.session.delete(phone_number)
    db.session.delete(person)
    db.session.commit()


def request_accepts(*mimetypes):
    best = request.accept_mimetypes.best_match(mimetypes)
    return request.accept_mimetypes[best] and request.accept_mimetypes[best] >= request.accept_mimetypes['text/html']


def paginate_results(query_object, response_object=None, page=1, per_page=5):
    """
    Accepts a SQLAlchemy query object.
    Model must provide get_collection_object() and return a dict with it
    Returns a paginated CollectionPlusJSON instance
    """
    api_url_template = '/api/entry/?page={page}'
    if not response_object:
        response_object = CollectionPlusJSON()

    if (type(page) is not int) or (type(per_page) is not int):
        try:
            page = int(page)
            per_page = int(per_page)
        except (ValueError, TypeError):
            abort(400)

    if per_page != 5:
        api_url_template += '&per_page={per}'

    try:
        result_pages = query_object.paginate(page, per_page=per_page)
    except (ValueError, OverflowError):
        abort(400)
        
    next_page = result_pages.next_num if result_pages.has_next else None
    prev_page = result_pages.prev_num if result_pages.page > 1 else None
    result = result_pages.items

    if result_pages.page != 1:
        response_object.append_link(api_url_template.format(page=1, per=per_page), 'first', 'First')

    if prev_page:
        response_object.append_link(api_url_template.format(page=prev_page, per=per_page), 'prev', 'Previous')

    for page in result_pages.iter_pages():
        if page is not None:
            if page == result_pages.page:
                rel = 'self'
            else:
                rel = 'more'
            response_object.append_link(api_url_template.format(page=page, per=per_page), rel, str(page))
        else:
            response_object.append_link('#', '', '...')

    if next_page:
        response_object.append_link(api_url_template.format(page=next_page, per=per_page), 'next', 'Next')

    if result_pages.page != result_pages.pages:
        response_object.append_link(api_url_template.format(page=result_pages.pages, per=per_page), 'last', 'Last')

    for item in result:
        response_object.append_item(item.get_collection_object(short=True))

    return response_object


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
    if request.method == 'GET':
        if not request_accepts(COLLECTION_JSON):
            abort(406)
        # return paginated contact info
        response_object = paginate_results(
            Person.query.order_by(Person.last_name),
            page=request.args.get('page') or 1,
            per_page=request.args.get('per_page') or 5,
            response_object=CollectionPlusJSON(href=api_href)
        )
        return Response(str(response_object), mimetype=response_object.mimetype)
    else:
        if request.mimetype != COLLECTION_JSON:
            abort(415)
        pass  # assume POST? process new contact creation request


@app.route('/api/entry/<int:person_id>/', methods=['GET', 'DELETE', 'PATCH'])
def api_entry(person_id=None):
    if isinstance(person_id, int):
        api_href = '/api/entry/%d' % person_id
        if request.method == 'GET':
            if not request_accepts(COLLECTION_JSON):
                abort(406)
            # return person info
            response_object = CollectionPlusJSON(href=api_href)
            person = Person.query.get_or_404(person_id)
            response_object.append_item(person.get_collection_object())
            return Response(str(response_object), mimetype=response_object.mimetype)
        elif request.method == 'DELETE':
            # process contact deletion request
            try:
                delete_entry(person_id)
            except Exception as e:
                raise e
            else:
                return ('', 204)
        else:
            if request.mimetype != COLLECTION_JSON:
                abort(415)
            pass  # assume PATCH? process contact modification request
    else:
        abort(404)  # TODO: Create response body with collection+json 404 error body


@app.route('/api/search/')
def api_search():
    # TODO: requires python 2 until Flask-WhooshAlchemy supports python 3
    pass


if __name__ == '__main__':
    # generate_test_db()  # uncomment to generate test database
    whooshalchemy.whoosh_index(app, Person)  # TODO: figure out if this should be a scheduled task instead
    app.run()