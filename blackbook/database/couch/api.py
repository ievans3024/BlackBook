import datetime
import couchdb
import couchdb.mapping
import blackbook.database.couch.database
import blackbook.tools.tools
import blackbook.api.basecollection
import blackbook.api.errors

from blackbook.api import APIField
from blackbook.api import APIType
from blackbook.api import API
from blackbook.lib import collection_plus_json
from flask import Blueprint
from flask import current_app
from flask import request
from flask import Response
from flask import session

__author__ = 'ievans3024'


class CouchAPI(API):
    """Abstract Base Class for interfacing with couch Document classes"""

    db = APIField(couchdb.Database)
    model = APIType(couchdb.mapping.Document)

    def _generate_document(self, *args, href='/', **kwargs):
        """
        Generate a document

        Implementations should return a collection+json document object.
        """
        raise NotImplementedError()

    def _get_authenticated_user(self, user_api, session_api):
        user = None
        if session.get("id"):
            sessions_by_token = session_api.model.by_token(key=session["id"])
            if sessions_by_token.rows:
                get_session = sessions_by_token.rows[0]
                if get_session.expiry > datetime.datetime.now():
                    user = user_api.model.load(self.db, get_session.user)
        return user

    def delete(self, *args, **kwargs):
        raise NotImplementedError()

    def get(self, *args, **kwargs):
        raise NotImplementedError()

    def head(self, *args, **kwargs):
        raise NotImplementedError()

    def options(self, *args, **kwargs):
        raise NotImplementedError()

    def patch(self, *args, **kwargs):
        raise NotImplementedError()

    def post(self, *args, **kwargs):
        raise NotImplementedError()

    def put(self, *args, **kwargs):
        raise NotImplementedError()

    def search(self, *args, **kwargs):
        raise NotImplementedError()


class Contact(CouchAPI):
    """
    Contact API class

    /contact/[?[after=<id>][before=<id>][q=<query>][name=<name>][surname=<surname>][email=<email>][phone=<phone_number>]]

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
            - requires authenticated user
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

        POST: unsupported
            - HTTP 405 response
            - All collection fields will be empty, if possible, except error
            - collection.error will contain 405 error code, title and message


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


    /user/<user_id>/contacts/[?[page=<pagenum>][q=<query>][name=<name>][surname=<surname>][email=<email>][phone=<phone_number>]]

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

    """

    def __init__(self, db):
        super(Contact, self).__init__(db, blackbook.database.couch.models.Contact)

    def _generate_document(self, *args, href='/contact/', **kwargs):
        """
        Generate a Contact document representation.
        :param **kwargs:
        """
        document = blackbook.api.basecollection.ContactCollection(href=href)
        return document

    def delete(self, contact_id=None, *args, **kwargs):
        user_api = User(self.db)
        session_api = Session(self.db)

        user = self._get_authenticated_user(user_api, session_api)

        if not blackbook.tools.tools.check_angular_xsrf():
            document = self._generate_document()
            document.error = blackbook.api.errors.APIBadRequestError()
            pass

        if not user:
            document = self._generate_document()
            document.error = blackbook.api.errors.APIUnauthorizedError()
            return Response(response=str(document), status=int(document.error.code), mimetype=document.mimetype)

        if contact_id:
            contact = self.model.load(id=contact_id)

            if (not contact) or \
                    (
                        contact.user != user.id and
                        not user.has_permission(
                            self.db,
                            ".".join([self.db.name, "delete", self.model.__name__.lower()])
                        )
                    ):
                document = self._generate_document()
                document.error = blackbook.api.errors.APINotFoundError()
                return Response(response=str(document), status=int(document.error.code), mimetype=document.mimetype)
            else:
                self.db.delete(contact)
                return Response(response="", status=204)

    def get(self, contact_id=None, user_id=None):

        user_api = User(self.db)
        session_api = Session(self.db)

        user = self._get_authenticated_user(user_api, session_api)
        document = self._generate_document()
        spec_properties = self.api_spec["properties"]

        if not self._request_origin_consistent():
            # TODO: handle bad CSRF -- APIBadRequestError?
            pass

        if not user:
            document.error = blackbook.api.errors.APIUnauthorizedError()
            return Response(str(document), status=int(document.error.code), mimetype=document.mimetype)

        if contact_id:
            contact = self.model.load(id=contact_id)
            template_data = self.api_spec["template_data"]["update"]
            template_meta = self.api_spec["template_meta"]["update"]

            if (not contact) or \
                    (
                        contact.user != user.id and
                        not user.has_permission(
                            self.db,
                            ".".join([self.db.name, "read", self.model.__name__.lower()])
                        )
                    ):
                document.error = blackbook.api.errors.APINotFoundError()
                return Response(str(document), status=int(document.error.code), mimetype=document.mimetype)
            else:
                contacts = [contact]
        else:
            prev_viewargs = {}
            next_viewargs = {}
            _range = {}
            template_data = self.api_spec["template_data"]["create"]
            template_meta = self.api_spec["template_meta"]["create"]

            if request.args.get("end"):
                _range["endkey_docid"] = request.args.get("end")
            if request.args.get("start"):
                _range["startkey_docid"] = request.args.get("start")

            if (request.args.get("start") and not request.args.get("end")) or \
                    (request.args.get("end") and not request.args.get("start")):
                _range["limit"] = current_app.config.get("API_PAGINATION_PER_PAGE") or 10

            if user_id:
                if not user_api.model.load(self.db, id=user_id):
                    document.error = blackbook.api.errors.APINotFoundError()
                    return Response(response=str(document), status=int(document.error.code), mimetype=document.mimetype)
                if user.id == user_id or user.has_permission(
                        ".".join([self.db.name, "read", user_api.model.__name__.lower()])):
                    contacts = self.model.by_user(key=user_id, **_range)
                    viewfunc = self.model.by_user
                    if _range.get("endkey_docid"):
                        next_viewargs.update(key=user_id, startkey_docid=_range["endkey_docid"], limit=2)
                    if _range.get("startkey_docid"):
                        prev_viewargs.update(key=user_id, endkey_docid=_range["startkey_docid"], limit=2)
                else:
                    document.error = blackbook.api.errors.APINotFoundError()
                    return Response(str(document), status=int(document.error.code), mimetype=document.mimetype)
            elif user.has_permission(".".join([self.db.name, "read", self.model.__name__.lower()])):
                contacts = self.model.view(self.db, "_all_docs", **_range)
                viewfunc = self.model.view
                if _range.get("endkey_docid"):
                    next_viewargs.update(viewname="_all_docs", startkey_docid=_range["endkey_docid"], limit=2)
                if _range.get("startkey_docid"):
                    prev_viewargs.update(viewname="_all_docs", endkey_docid=_range["startkey_docid"], limit=2)
            else:
                contacts = self.model.by_user(key=user.id, **_range)
                viewfunc = self.model.by_user
                if _range.get("endkey_docid"):
                    next_viewargs.update(key=user.id, startkey_docid=_range["endkey_docid"], limit=2)
                if _range.get("startkey_docid"):
                    prev_viewargs.update(key=user.id, endkey_docid=_range["startkey_docid"], limit=2)
                
            if _range.get("startkey_docid"):
                # get prev page link, if applicable
                prev_contacts_endkey = viewfunc(self.db, **prev_viewargs)
                if prev_contacts_endkey.rows:
                    key = prev_contacts_endkey.rows[0].id
                    url = request.url_rule + "?end={docid}".format(docid=key)
                    document.links.append(collection_plus_json.Link(href=url, rel="prev", name="Previous", prompt="<"))
            if _range.get("endkey_docid"):
                # get next page link, if applicable
                next_contacts_startkey = viewfunc(self.db, **next_viewargs)
                if next_contacts_startkey.rows:
                    key = next_contacts_startkey.rows[1].id
                    url = request.url_rule + "?start={docid}".format(docid=key)
                    document.links.append(collection_plus_json.Link(href=url, rel="next", name="Next", prompt=">"))

        for contact in contacts:
            document.items.append(
                collection_plus_json.Item(
                    href="{endpoint}{id}/".format(endpoint=self.api_spec["endpoint"], id=contact.id),
                    data=[
                        prop["data"] for prop in spec_properties
                        # owning users have <dbname>.read.<modelname>.<propertyname>
                        # admin users have <dbname>.read.<modelname>
                        if prop["permissions"]["public"] or user.has_permission(*prop["permisisons"]["read"])
                        ],
                    links=[
                        collection_plus_json.Link(
                            href="{endpoint}{id}/".format(endpoint=user_api.api_spec["endpoint"], id=user.id),
                            rel="owner",
                            prompt="Created by {name}".format(user.name)
                        )
                    ]
                )
            )

        # authenticated users have permission <dbname>.update.<modelname>
        # therefore they can see the update template
        if template_meta["permissions"]["public"] or \
                user.has_permission(self.db, *template_meta["permissions"]["read"]):
            document.template = collection_plus_json.Template(data=template_data)

        return Response(response=str(document), mimetype=document.mimetype)

    def head(self, *args, **kwargs):
        pass

    def options(self, *args, **kwargs):
        pass

    def patch(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        pass


class Session(CouchAPI):
    """
    Session API Class

    /session/

        GET: get authentication information
            - HTTP 200 response
            - if authenticated and authentication has not expired or not authenticated:
                - if authenticated:
                    - collection.items will be a one-item list containing the user's session info
                    - collection.template will be empty
                - if not authenticated:
                    - collection.items will be empty
                    - collection.template will contain creation template (login form)
            - if authenticated and authentication has expired:
                - HTTP 419 response
                - collection.items will be empty
                - collection.template will contain creation template (login form)
                - collection.error will contain 419 error code, title and message

        POST: create a new session (log in)
            - requires complete creation template
            - if creation template is complete and login is successful:
                - HTTP 201 response
                - session var id set to Session.token value
                - collection.items will be a one-item list containing new session info
                - collection.template will be empty
            - if creation template is complete and login is unsuccessful:
                - HTTP 401 response
                - collection.items will be empty
                - collection.template will contain creation template
                - collection.error will contain 401 error code, title and message
            - if creation template is not complete:
                - HTTP 400 response
                - collection.items will be empty
                - collection.template will contain creation template
                - collection.error will contain 400 error code, title and message


    /session/<token>/

        GET: get information about a session
            - requires authenticated user
                - if not authenticated:
                    - HTTP 401 response
                    - collection.items will be empty
                    - collection.template will contain creation template
                    - collection.error will contain 401 error code, title and message
                - if authenticated and session.user == user.id:
                    - HTTP 200 response
                    - collection.items will be a one-item list containing the session info
                    - collection.template will be empty
                - if (authenticated and session.user != user.id) or token does not exist:
                    - HTTP 404 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 404 error code, title and message

        PUT: update session expiry
            - requires authenticated user
                - if not authenticated:
                    - HTTP 401 response
                    - collection.items will be empty
                    - collection.template will contain creation template
                    - collection.error will contain 401 error code, title and message
                - if authenticated and session.user == user.id:
                    - HTTP 200 response
                    - session.expiry gets updated
                    - collection.items will be a one-item list containing updated session info
                    - collection.template will be empty
                - if (authenticated and session.user != user.id) or token does not exist:
                    - HTTP 404 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 404 error code, title and message

        PATCH: update session expiry
            - clone functionality of PUT method for this endpoint

        POST: unsupported
            - HTTP 405 response
            - All collection fields will be empty, if possible, except error
            - collection.error will contain 405 error code, title and message

        DELETE: de-authenticate and delete the current session (log out)
            - requires authenticated user
                - if not authenticated:
                    - HTTP 401 response
                    - collection.items will be empty
                    - collection.template will contain creation template
                    - collection.error will contain 401 error code, title and message
                - if authenticated and session.user == user.id:
                    - HTTP 204 response
                    - No response body
                - if (authenticated and session.user != user.id) or token does not exist:
                    - HTTP 404 response
                    - collection.items and collection.template will be empty
                    - collection.error will contain 404 error code, title and message
    """

    def __init__(self, db):
        super(Session, self).__init__(db, blackbook.database.couch.models.Session)

    def _generate_document(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        pass

    def head(self, *args, **kwargs):
        pass

    def options(self, *args, **kwargs):
        pass

    def patch(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        pass


class User(CouchAPI):
    """
    User API class

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

    """

    def __init__(self, db):
        super(User, self).__init__(db, blackbook.database.couch.models.User)

    def _generate_document(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        pass

    def head(self, *args, **kwargs):
        pass

    def options(self, *args, **kwargs):
        pass

    def patch(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        pass


def init_api(app):

    database = blackbook.database.couch.database.init_db(app)

    api_blueprint = Blueprint("api", __name__, url_prefix="/api")  # TODO: use config API_ROOT

    def api_root():
        document = collection_plus_json.Collection(
            href="/api/",  # TODO: use config API_ROOT
            links=[
                collection_plus_json.Link(href="/api/contact/", rel="more", prompt="Contacts Endpoint"),
                collection_plus_json.Link(href="/api/user/", rel="more", prompt="Users Endpoint"),
                collection_plus_json.Link(href="/api/session/", rel="more", prompt="Sessions API")
            ]
        )
        if request.method in {"GET", "OPTIONS"}:
            return Response(response=document, mimetype=document.mimetype)
        else:
            return Response()

    contact_view = Contact(database).as_view('contact_api')

    api_blueprint.add_url_rule('/', view_func=api_root, methods=["GET", "HEAD", "OPTIONS"])
    api_blueprint.add_url_rule('/contact/', defaults={'user_id': None}, view_func=contact_view, methods=["GET", "POST"])
    api_blueprint.add_url_rule('/contact/<contact_id>/', defaults={'user_id': None, 'contact_id': None},
                               view_func=contact_view, methods=["GET", "PATCH", "PUT", "DELETE"])
    api_blueprint.add_url_rule('/user/<user_id>/contacts/', defaults={'user_id': None},
                               view_func=contact_view, methods=["GET", "POST"])

    return api_blueprint
