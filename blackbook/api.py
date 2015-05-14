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
        - optionally allows public creation of user accounts
        - requires completed creation form
            - if (not authenticated and public registration is on) or (authenticated admin user):
                - if form is complete:
                    - HTTP 201 response
                    - collection.items will contain a one-item list of the new user's information
                    - collection.template will contain the creation template
                - if form is incomplete:
                    - HTTP 400 response
                    - collection.items will be empty
                    - collection.template will contain the creation template
                    - collection.error will contain 400 error code, title and message
            - if not authenticated and public registration is off:
                - HTTP 401 response
                - collection.items will be empty
                - collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated non-admin user:
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
            - if authenticated:
                - non-admin users may only retrieve their own info
                - admin users may retrieve info about any user
                - certain info (such as passwords) cannot be retrieved through the api
                - if (non-admin user and <id> == user.id) or (admin user):
                    - HTTP 200 response
                    - collection.items will contain a one-item list with the user's information
                    - collection.template will contain the update template
                - if non-admin user and (<id> != user.id or <id> does not exist):
                    - HTTP 403 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 403 error code, title and message
                - if admin user and <id> does not exist:
                    - HTTP 404 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 404 error code, title and message

    PUT: update information about a specific user
        - requires authenticated user and complete template
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - non-admin users may only update themselves
                - admin users may update any user
                - certain info (such as passwords) can only be modified by a user's own self through the api
                - if (non-admin user and <id> == user.id) or (admin user):
                    - if template complete:
                        - HTTP 200 response
                        - collection.items will contain a one-item list with the user's updated information
                        - collection.template will contain the update template
                    - if template incomplete:
                        - 400 HTTP response
                        - collection.items will be empty
                        - collection.template will contain update template
                        - collection.error will contain 400 error code, title and message
                - if non-admin user and (<id> != user.id or <id> does not exist):
                    - HTTP 403 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 403 error code, title and message
                - if admin user and <id> does not exist:
                    - HTTP 404 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 404 error code, title and message

    PATCH: update information about a specific user
        - requires authenticated user and partial or complete template
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - non-admin users may only update themselves
                - admin users may update any user
                - certain info (such as passwords) can only be modified by a user's own self through the api
                - data in submitted template that does not match the server's template will be ignored
                - if (non-admin user and <id> == user.id) or (admin user):
                    - if template contains matching data:
                        - HTTP 200 response
                        - collection.items will contain a one-item list with the user's updated information
                        - collection.template will contain the update template
                    - if template does not contain any matching data:
                        - 400 HTTP response
                        - collection.items will be empty
                        - collection.template will contain update template
                        - collection.error will contain 400 error code, title and message
                - if non-admin user and (<id> != user.id or <id> does not exist):
                    - HTTP 403 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 403 error code, title and message
                - if admin user and <id> does not exist:
                    - HTTP 404 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 404 error code, title and message

    DELETE: delete a specific user
        - requires authenticated user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - if (non-admin user and <id> == user.id) or (admin user):
                    - HTTP 204 response
                    - No body
                - if non-admin user and (<id> != user.id or <id> does not exist):
                    - HTTP 403 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 403 error code, title and message
                - if admin and <id> does not exist:
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
                - admin users may view contacts for all users
                - if (non-admin user and <id> == user.id) or (admin user):
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
                - if non-admin user and (<id> != user.id or <id> does not exist):
                    - HTTP 403 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 403 error code, title and message
                - if admin user and <id> does not exist:
                    - HTTP 404 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 404 error code, title and message

    POST: create a new contact for a particular user
        - requires authenticated user and completed creation form
            - if not authenticated:
                - unauthenticated users cannot create new contacts
                - HTTP 401 response
                - collection.items will be empty
                - collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if (authenticated non-admin and <id> == user.id) or (authenticated admin user):
                - non-admins may only create contacts for themselves
                - admins may create contacts for any user
                - if form is complete:
                    - HTTP 201 response
                    - collection.items will contain a one-item list of the new user's information
                    - collection.template will contain the creation template
                - if form is incomplete:
                    - HTTP 400 response
                    - collection.items will be empty
                    - collection.template will contain the creation template
                    - collection.error will contain 400 error code, title and message
            - if authenticated non-admin and <id> != user.id:
                - non-admins may not create contacts for other users
                - HTTP 403 response
                - collection.items and collection.template will be empty
                - collection.error will contain 403 error code, title and message


/contact/[?[page=<pagenum>][q=<query>][name=<name>][surname=<surname>][email=<email>][phone=<phone_number>]]

    GET: retrieve list of contacts
        - requires authenticated admin user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - non-admin users may only view their own contacts
                - admin users may view contacts for all users
                - HTTP 200 response
                - collection.items will contain a paginated list of contacts
                - collection.links will contain a list of pagination links
                - collection.queries will contain a list of queries that can be performed
                    - q: general query/search (searches all fields)
                    - name: search by first name
                    - surname: search by last name
                    - email: search by email
                    - phone: search by phone number
                - collection.template will contain the creation template

    POST: create a new contact
        - requires authenticated user and completed creation form
            - if not authenticated:
                - unauthenticated users cannot create new contacts
                - HTTP 401 response
                - collection.items will be empty
                - collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - new contact will be associated with authenticated user
                - if form is complete:
                    - HTTP 201 response
                    - collection.items will contain a one-item list of the new user's information
                    - collection.template will contain the creation template
                - if form is incomplete:
                    - HTTP 400 response
                    - collection.items will be empty
                    - collection.template will contain the creation template
                    - collection.error will contain 400 error code, title and message


/contact/<id>/

    GET: retrieve information about a specific contact
        - requires authenticated admin user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - non-admin users may only view their own contacts
                - admin users may view contacts for all users
                - if (non-admin user and contact.user == user.id) or (admin user):
                    - HTTP 200 response
                    - collection.items will contain one-item list containing the contact's information
                    - collection.links will contain a one-link list containing a link to the contact's owner User
                        - link rel=owner
                    - collection.template will contain the update template
                - if non-admin user and (contact.user != user.id or <id> does not exist):
                    - HTTP 404 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 404 error code, title and message

    PUT: update information about a specific contact
        - requires authenticated user and complete template
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - non-admin users may only update their own contacts
                - admin users may update contacts for all users
                - if (non-admin user and contact.user == user.id) or (admin user):
                    - if template complete:
                        - HTTP 200 response
                        - collection.items will contain one-item list containing the contact's updated information
                        - collection.links will contain a one-link list containing a link to the contact's owner User
                            - link rel=owner
                        - collection.template will contain the update template
                    - if template incomplete:
                        - HTTP 400 response
                        - collection.items will be empty
                        - collection.template will contain the update template
                        - collection.error will contain 400 error code, title and message
                - if non-admin user and (contact.user != user.id or <id> does not exist):
                    - HTTP 404 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 404 error code, title and message

    PATCH: update information about a specific contact
        - requires authenticated user and partial or complete template
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - non-admin users may only update their own contacts
                - admin users may update contacts for all users
                - data in the submitted template that does not match the server's template will be ignored
                - if (non-admin user and contact.user == user.id) or (admin user):
                    - if template contains matching data:
                        - HTTP 200 response
                        - collection.items will contain one-item list containing the contact's updated information
                        - collection.links will contain a one-link list containing a link to the contact's owner User
                            - link rel=owner
                        - collection.template will contain the update template
                    - if template does not contain any matching data:
                        - HTTP 400 response
                        - collection.items will be empty
                        - collection.template will contain the update template
                        - collection.error will contain 400 error code, title and message
                - if non-admin user and (contact.user != user.id or <id> does not exist):
                    - HTTP 404 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 404 error code, title and message

    DELETE: delete a specific contact
        - requires authenticated user
            - if not authenticated:
                - HTTP 401 response
                - collection.items and collection.template will be empty
                - collection.error will contain 401 error code, title and message
            - if authenticated:
                - non-admin users may only delete their own contacts
                - admin users may delete any contact
                - if (non-admin user and contact.user == user.id) or (admin user):
                    - HTTP 204 response
                    - No body
                - if (non-admin user and contact.user != user.id) or <id> does not exist:
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