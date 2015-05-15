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

"""

import collection_plus_json
import couchdb
import couchdb.mapping
import blackbook.tools
import blackbook.database.models

from datetime import datetime
from flask import Blueprint, current_app, request, Response, session
from flask.views import MethodView


class APIType(object):
    """Descriptor for properties that need to a class or a subclass of such."""

    def __init__(self, cls):
        if isinstance(cls, type):
            self.cls = cls
        else:
            raise TypeError("Parameter 'cls' must be a class.")

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            if self.get_own_name(owner) in instance.__dict__.keys():
                return instance.__dict__.get(self.get_own_name(owner))
            else:
                raise AttributeError(
                    "'{cls}' object has no attribute '{name}'".format(
                        cls=owner.__name__,
                        name=self.get_own_name(owner)
                    )
                )

    def __set__(self, instance, value):
        if instance:
            if not (value is self.cls) or (issubclass(value, self.cls)):
                raise ValueError(
                    "Value must be {cls} or a subclass of it.".format(
                        cls=".".join([self.cls.__module__, self.cls.__name__])
                    )
                )
            instance.__dict__[self.get_own_name(type(instance))] = value

    def __delete__(self, instance):
        if instance:
            del instance.__dict__[self.get_own_name(type(instance))]

    def get_own_name(self, owner):
        for attr in dir(owner):
            if getattr(owner, attr) is self:
                return attr


class APIField(APIType):
    """Descriptor for properties that need to be an instance of a class or subclass of such."""

    def __set__(self, instance, value):
        if not isinstance(value, self.cls):
            raise TypeError(
                "Value must be an instance of {cls} or one of its subclasses.".format(
                    cls=".".join([self.cls.__module__, self.cls.__name__])
                )
            )
        instance.__dict__[self.get_own_name(type(instance))] = value


class ABC(MethodView):
    """Abstract Base Class for interfacing with couchdb Document classes"""

    db = APIField(couchdb.Database)
    model = APIType(couchdb.mapping.Document)

    def __init__(self, db, model):
        """
        Constructor
        :param db: The couchdb database to draw data from.
        :param model: The couchdb document class to represent data with.
        :return:
        """
        super(ABC, self).__init__()
        self.db = db
        self.model = model
        self.api_spec = blackbook.tools.merge_complex_dicts(
            *[
                {
                    k: v for k, v in db.get("_api/{cls}".format(cls=cls.__name__.lower())).items()
                } for cls in self.__class__.mro() if cls is not ABC and issubclass(cls, ABC)
            ]
        )

    @staticmethod
    def _request_origin_consistent():
        return request.headers.get("Origin") == current_app.config.get("SERVER_NAME")

    def _generate_document(self, *args, **kwargs):
        """
        Generate a document object

        Implementations should return a document object
        that can be manipulated and then serialized into
        a string to be returned in the HTTP response body.
        """
        raise NotImplementedError()

    def _get_authenticated_user(self):
        user = None
        if session.get("id"):
            sessions_by_token = Session.model.by_token(key=session["id"])
            if sessions_by_token.rows:
                get_session = sessions_by_token.rows[0]
                if get_session.expiry > datetime.now():
                    user = User.model.load(self.db, get_session.user)
        return user

    def delete(self, *args, **kwargs):
        raise NotImplementedError()

    def get(self, *args, **kwargs):
        raise NotImplementedError()

    def patch(self, *args, **kwargs):
        raise NotImplementedError()

    def post(self, *args, **kwargs):
        raise NotImplementedError()

    def put(self, *args, **kwargs):
        raise NotImplementedError()

    def search(self, *args, **kwargs):
        raise NotImplementedError()


class APIError(collection_plus_json.Error, BaseException):
    """
    Wrapper class for API Errors

    May be raised as a python exception, i.e.:
        raise APIError()

    May be inserted into a collection_plus_json.Collection instance, i.e.:
        collection_plus_json.Collection(href="/foo/", error=APIError())

    Convenience classes that subclass this:

        APINotFoundError

    These convenience classes are to allow for catching certain types of errors, e.g.:

        try:
            # stuff...
        except APINotFoundError:
            # handle resource not found
        else:
            # let other types of APIErrors get raised

    Additionally, easier than typing out common errors every time they come up:

        collection_plus_json.Collection(href="/foo/", error=APINotFoundError())

    instead of

        collection_plus_json.Collection(
            href="/foo/",
            error=APIError(
                code="404",
                title="Not Found",
                message="The server could not find the requested resource."
            )
        )

    """

    def __init__(self,
                 code="500",
                 title="Internal Server Error",
                 message="The server could not complete the request because it encountered an error internally.",
                 **kwargs
                 ):
        """
        APIError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APIError, self).__init__(code=code, message=message, title=title, **kwargs)


class APINotFoundError(APIError):
    """Convenience class for HTTP 404 errors"""

    def __init__(self,
                 code="404",
                 title="Not Found",
                 message="The server could not find the requested resource.",
                 **kwargs
                 ):
        """
        APINotFoundError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APINotFoundError, self).__init__(code=code, title=title, message=message, **kwargs)


class Contact(ABC):
    """
    Contact API class

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

    def __init__(self, db):
        super(Contact, self).__init__(db, blackbook.database.models.Contact)

    def _generate_document(self, *args, **kwargs):
        """Generate a Contact document representation."""

        document = collection_plus_json.Collection(self.api_spec["endpoint"])
        document.template = collection_plus_json.Template(data=self.api_spec["template_data"]["create"])
        return document

    def delete(self, *args, **kwargs):
        pass

    def get(self, _id=None):

        user = self._get_authenticated_user()
        document = self._generate_document()

        # check request header for consistent "Origin" HTTP header
        if not self._request_origin_consistent():
            pass

        # check session vars for authenticated session
        if session.get("id"):
            pass

    def patch(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        pass


class Session(ABC):

    def __init__(self, db):
        super(Session, self).__init__(db, blackbook.database.models.Session)

    def delete(self, *args, **kwargs):
        pass

    def generate_document(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        pass

    def patch(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        pass


class User(ABC):

    def __init__(self, db):
        super(User, self).__init__(db, blackbook.database.models.User)

    def delete(self, *args, **kwargs):
        pass

    def generate_document(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        pass

    def patch(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        pass