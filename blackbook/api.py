__author__ = 'ievans3024'

# TODO: API using Blueprint instance and MethodView subclasses
#   (couchdb <-> couchdb model classes <-> API MethodView subclasses <-> AngularJS/Client)
# TODO: Convert to https://github.com/ievans3024/CollectionPlusJSON
# TODO: API Error classes
#   e.g., APINotFoundError, APIForbiddenError, etc.

"""
/user/[?[page=<pagenum>][username=<name>][email=<email>]]

    GET: retrieve list of users
        - serves creation template
        - requires authenticated admin user to see user list
        - optionally requires authenticated admin user to see creation template
        - if not authenticated:
            - if public registration is off:
                - HTTP 401 response
                - collection.items and collection.template will be empty
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
                - collection.queries will contain a list of queries that can be performed
                    - username: search the list by username
                    - email: search the list by email
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
        - if public registration is on:
            - if form is complete:
                - HTTP 201 response
                - collection.items will contain a one-item list of the new user's information
                - collection.template will contain the update template
            - if form is incomplete:
                - HTTP 400 response
                - collection.items will be empty
                - collection.template will contain the creation template
                - collection.error will contain 400 error code, title and message
        - if authenticated:
            - if not authorized:
                - HTTP 403 response
                - collection.items and collection.template will be empty
                - collection.error will contain 403 error code, title and message
            - if authorized:
                - if form is complete:
                    - HTTP 201 response
                    - collection.items will contain a one-item list of the new user's information
                    - collection.template will contain the update template
                - if form is incomplete:
                    - HTTP 400 response
                    - collection.items will be empty
                    - collection.template will contain the creation template
                    - collection.error will contain 400 error code, title and message


/user/<id>/

    GET: retrieve information about a specific user
        - serves update template
        - requires authenticated user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - non-admin users may only retrieve their own info
                - if <id> == user.id:
                    - HTTP 200 response
                    - collection.items will contain a one-item list with the user's information
                    - collection.template will contain the update template
                - if <id> != user.id:
                    - HTTP 403 response (regardless of whether <id> exists in the system)
                    - collection.items and collection.template will be empty
                    - collection.error will contain 403 error code, title and message
            - admin users may retrieve info about any user
                - certain info (such as passwords--hashed or plaintext,) is not retrievable through the api
                - 404 response if <id> does not exist

    PUT: update information about a specific user
        - requires authenticated user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - non-admin users may only update themselves
                - if <id> == user.id:
                    - HTTP 200 response
                    - collection.items will contain a one-item list with the user's updated information
                    - collection.template will contain the update template
                - if <id> != user.id:
                    - HTTP 403 response (regardless of whether <id> exists in the system)
                    - collection.items and collection.template will be empty
                    - collection.error will contain 403 error code, title and message
            - admin users may update any user
                - certain info (such as passwords,) is not modifiable by admins through the api
                - if <id> == user.id:
                    - HTTP 200 response
                    - collection.items will contain a one-item list with the user's updated information
                    - collection.template will contain the update template
                - if <id> does not exist:
                    - HTTP 404 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 404 error code, title and message
        - requires complete update template
            - if authenticated:
                - if not complete:
                    - 400 HTTP response
                    - collection.items will be empty
                    - collection.template will contain update template
                    - collection.error will contain 400 error code, title and message

    PATCH: update information about a specific user
        - requires authenticated user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - non-admin users may only update themselves
                - if <id> == user.id:
                    - HTTP 200 response
                    - collection.items will contain a one-item list with the user's updated information
                    - collection.template will contain the update template
                - if <id> != user.id:
                    - HTTP 403 response (regardless of whether <id> exists in the system)
                    - collection.items and collection.template will be empty
                    - collection.error will contain 403 error code, title and message
            - admin users may update any user
                - certain info (such as passwords) is not modifiable by admins through the api
                - if <id> exists:
                    - HTTP 200 response
                    - collection.items will contain a one-item list with the user's updated information
                    - collection.template will contain the update template
                - if <id> does not exist:
                    - HTTP 404 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 404 error code, title and message
        - accepts partial or complete update template
            - data that is not part of the template as stored in the server's api spec will be ignored
            - if authenticated:
                - if no matching data items exist in the supplied template:
                    - 400 HTTP response
                    - collection.items will be empty
                    - collection.template will contain update template
                    - collection.error will contain 400 error code, title and message

    DELETE: delete a specific user
        - requires authenticated user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - non-admin users may only delete themselves
                - if <id> == user.id:
                    - HTTP 204 response
                    - No body
                - if <id> != user.id:
                    - HTTP 403 response (regardless of whether <id> exists in the system)
                    - collection.items and collection.template will be empty
                    - collection.error will contain 403 error code, title and message
            - admin users may delete any user
                - if <id> exists:
                    - HTTP 204 response
                    - no body
                - if <id> does not exist:
                    - HTTP 404 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 404 error code, title and message


/user/<id>/contacts/[?[page=<pagenum>][q=<query>][name=<name>][surname=<surname>][email=<email>][phone=<phone_number>]]

    GET: retrieve list of contacts for a particular user
        - only displays contacts a specific user has created
        - requires authenticated user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - non-admin users may only view their own contacts
                    - if <id> == user.id:
                        - HTTP 200 response
                        - collection.items will contain a paginated list of the user's contacts
                        - collection.links will contain a list of pagination links
                        - collection.queries will contain a list of queries that can be performed
                            - q: general query/search (searches all fields)
                            - name: search by first name
                            - surname: search by last name
                            - email: search by email
                            - phone: search by phone number
                        - collection.template will contain the creation template
                    - if <id> != user.id:
                        - HTTP 403 response (regardless of whether <id> exists in the system)
                        - collection.items and collection.template will be empty
                        - collection.error will contain 403 error code, title and message
                - admin users may view contacts for all users
                    - if <id> exists:
                        - HTTP 200 response
                        - collection.items will contain a paginated list of the user's contacts
                        - collection.links will contain a list of pagination links
                            - also contains a special "rel=owner" link, referring to the owning user
                        - collection.queries will contain a list of queries that can be performed
                            - q: general query/search (searches all fields)
                            - name: search by first name
                            - surname: search by last name
                            - email: search by email
                            - phone: search by phone number
                        - collection.template will contain the creation template
                    - if <id> does not exist:
                        - HTTP 404 response
                        - collection.items and collection.template will be empty
                        - collection.error will contain 404 error code, title and message

    POST: create a new contact for a particular user
        - requires authenticated user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - non-admin users may only create new contacts for themselves
                    - if <id> == user.id:
                        - HTTP 201 response
                        - collection.items will contain one-item list containing the new contact's information
                        - collection.template will contain the update template
                    - if <id> != user.id:
                        - HTTP 403 response (regardless of whether <id> exists in the system)
                        - collection.items and collection.template will be empty
                        - collection.error will contain 403 error code, title and message
                - admin users may create contacts for anyone
                    - HTTP 201 response
                    - collection.items will contain one-item list containing the new contact's information
                    - collection.links will contain a "rel=owner" link pointing to the new contact's owner User
                    - collection.template will contain the update template


/contact/[?[page=<pagenum>][q=<query>][name=<name>][surname=<surname>][email=<email>][phone=<phone_number>]]

    GET: retrieve list of contacts
        - requires authenticated admin user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - non-admin users may only view their own contacts
                    - HTTP 200 response
                    - collection.items will contain a paginated list of the user's contacts
                    - collection.links will contain a list of pagination links
                    - collection.queries will contain a list of queries that can be performed
                        - q: general query/search (searches all fields)
                        - name: search by first name
                        - surname: search by last name
                        - email: search by email
                        - phone: search by phone number
                    - collection.template will contain the creation template
                - admin users may view contacts for all users
                    - HTTP 200 response
                    - collection.items will contain a paginated list of existing contacts for all users
                    - collection.links will contain a list of pagination links
                    - collection.queries will contain a list of queries that can be performed
                        - q: general query/search (searches all fields)
                        - name: search by first name
                        - surname: search by last name
                        - email: search by email
                        - phone: search by phone number
                    - collection.template will contain the creation template

    POST: create a new contact
        - requires authenticated user
            - contact will be associated with authenticated user's contact list
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - HTTP 201 response
                - collection.items will contain one-item list containing the new contact's information
                - collection.template will contain the update template


/contact/<id>/

    GET: retrieve information about a specific contact
        - requires authenticated user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - non-admin users may only see their own contacts
                    - if contact.user == user.id:
                        - HTTP 200 response
                        - collection.items will contain a one-item list containing the contact's information
                        - collection.template will contain the update template
                    - if contact.user != user.id or <id> does not exist:
                        - HTTP 404 response
                        - collection.items and collection.template will be empty
                        - collection.errors will contain 404 error code, title and message
                - admin users may see all contacts
                    - if <id> exists:
                        - HTTP 200 response
                        - collection.items will contain a one-item list containing the contact's information
                        - collection.template will contain the update template
                    - if <id> does not exist:
                        - HTTP 404 response
                        - collection.items and collection.template will be empty
                        - collection.errors will contain 404 error code, title and message

    PUT: update information about a specific contact
        - requires authenticated user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - non-admin users may only update their own contacts
                    - if contact.user == user.id:
                        - HTTP 200 response
                        - collection.items will contain a one-item list containing the updated contact information
                        - collection.template will contain the update template
                    - if contact.user != user.id or <id> does not exist:
                        - HTTP 404 response
                        - collection.items and collection.template will be empty
                        - collection.errors will contain 404 error code, title and message
                - admin users may update all contacts
                    - if <id> exists:
                        - HTTP 200 response
                        - collection.items will contain a one-item list containing the updated contact information
                        - collection.template will contain the update template
                    - if <id> does not exist:
                        - HTTP 404 response
                        - collection.items and collection.template will be empty
                        - collection.errors will contain 404 error code, title and message
        - only accepts complete update template:
            - if template not complete:
                - 400 HTTP response
                - collection.items will be empty
                - collection.template will contain update template
                - collection.error will contain 400 error code, title and message

    PATCH: update information about a specific contact
        - requires authenticated user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - non-admin users may only update their own contacts
                    - if contact.user == user.id:
                        - HTTP 200 response
                        - collection.items will contain a one-item list containing the updated contact information
                        - collection.template will contain the update template
                    - if contact.user != user.id or <id> does not exist:
                        - HTTP 404 response
                        - collection.items and collection.template will be empty
                        - collection.errors will contain 404 error code, title and message
                - admin users may update all contacts
                    - if <id> exists:
                        - HTTP 200 response
                        - collection.items will contain a one-item list containing the updated contact information
                        - collection.template will contain the update template
                    - if <id> does not exist:
                        - HTTP 404 response
                        - collection.items and collection.template will be empty
                        - collection.errors will contain 404 error code, title and message
        - accepts partial or complete update template:
            - data that is not part of the template as stored in the server's api spec will be ignored
            - if no matching data items exist in the supplied template:
                - 400 HTTP response
                - collection.items will be empty
                - collection.template will contain update template
                - collection.error will contain 400 error code, title and message

    DELETE: delete a specific contact
        - requires authenticated user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - non-admin users may only delete their own contacts
                - if contact.user == user.id:
                    - HTTP 204 response
                    - No body
                - if contact.user != user.id:
                    - HTTP 404 response (regardless of whether <id> exists in the system)
                    - collection.items and collection.template will be empty
                    - collection.error will contain 404 error code, title and message
            - admin users may delete any contact
                - if <id> exists:
                    - HTTP 204 response
                    - no body
                - if <id> does not exist:
                    - HTTP 404 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 404 error code, title and message


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