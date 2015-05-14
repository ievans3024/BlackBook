__author__ = 'ievans3024'

# TODO: API using Blueprint instance and MethodView subclasses
#   (couchdb <-> couchdb model classes <-> API MethodView subclasses <-> AngularJS/Client)
# TODO: Convert to https://github.com/ievans3024/CollectionPlusJSON
# TODO: API Error classes
#   e.g., APINotFoundError, APIForbiddenError, etc.

"""
/user/[?[page=<pagenum>][q=<query>][name=<name>][surname=<surname>][email=<email>][phone=<phone_number>]]

    GET: retrieve list of users
        - serves creation template
        - requires authenticated admin user to see user list
        - optionally requires authenticated admin user to see creation template
        - if not authenticated:
            - if public registration is off:
                - HTTP 401 response
                - collection.items will be empty
                - collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if public registration is on:
                - HTTP 200 response
                - collection.items will be empty
                - collection.template will contain creation template
        - if authenticated:
            - if not authorized:
                - HTTP 403 response
                - collection.items and collection.template will be empty
                - collection.error will contain 403 error code, title and message
            - if authorized:
                - HTTP 200 response
                - collection.items will contain a paginated list of users
                - collection.links will contain a list of pagination links
                - collection.template will contain creation template

    POST: create a new user
        - only accepts creation template
        - authenticated users must be admins
        - optionally requires authenticated admin user to create new users (public registration turned off)
        - if public registration is off:
            - if not authenticated:
                - HTTP 401 response
                - collection.items will be empty
                - collection.template will be empty
                - collection.error will contain 401 error code, title and message
        - if authenticated:
            - if not authorized:
                - HTTP 403 response
                - collection.items and collection.template will be empty
                - collection.error will contain 403 error code, title and message

/user/<id>/

    GET: retrieve information about a specific user
        - serves update template
        - requires authenticated user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - non-admin users may only retrieve their own info
                -if <id> == user.id:
                    - HTTP 200
                    - collection.items will contain a one-item list with the user's information
                    - collection.
                - 403 response if <id> != User.id, regardless if <id> exists in the system
                - collection.items and collection.template will be empty
            - admin users may retrieve info about any user
                - certain info (such as passwords--hashed or plaintext,) is not retrievable through the api
                - 404 response if <id> does not exist

    PUT: update information about a specific user
        - requires authenticated user is updating themselves, or is an admin user
        - only accepts complete update template
        - 403 if authenticated but not authorized, 401 if not authenticated

    PATCH: update information about a specific user
        - requires authenticated user is updating themselves, or is an admin user
        - accepts partial or complete update template
        - 403 if authenticated but not authorized, 401 if not authenticated

    DELETE: delete a specific user
        - requires authenticated admin user and user is not themselves
        - 403 if authenticated but not authorized, 401 if not authenticated

/contact/

    GET: retrieve list of contacts
        - serves creation template
        - list will be empty if token associated with authenticated user is not present
        - only lists contacts created by the authenticated user (multi-user system)

    POST: create a new contact
        - only accepts creation template
        - requires token associated with authenticated user
        - only adds contact's info to authenticated user's contact list

/contact/<id>/

    GET: retrieve information about a specific contact
        - requires token associated with authenticated user
        - 404s if <id> is not in User.contacts, regardless of whether <id> exists in system
        - serves update template

    PUT: update information about a specific contact
        - requires token associated with authenticated user
        - 404s if <id> is not in User.contacts, regardless of whether <id> exists in system

    PATCH:

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