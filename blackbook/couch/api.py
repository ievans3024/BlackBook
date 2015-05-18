__author__ = 'ievans3024'

from datetime import datetime

import couchdb
import couchdb.mapping
from flask import Blueprint, current_app, request, Response, session
from flask.views import MethodView

from blackbook.lib import collection_plus_json
import blackbook.tools
import blackbook.couch.database
import blackbook.couch.models


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
    """Abstract Base Class for interfacing with couch Document classes"""

    db = APIField(couchdb.Database)
    model = APIType(couchdb.mapping.Document)

    def __init__(self, db, model):
        """
        Constructor
        :param db: The couch database_old to draw data from.
        :param model: The couch document class to represent data with.
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

    def _get_authenticated_user(self, user_api, session_api):
        user = None
        if session.get("id"):
            sessions_by_token = session_api.model.by_token(key=session["id"])
            if sessions_by_token.rows:
                get_session = sessions_by_token.rows[0]
                if get_session.expiry > datetime.now():
                    user = user_api.model.load(self.db, get_session.user)
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

        APIBadRequestError              400 Bad Request
        APINotAuthorizedError           401 Not Authorized
        APIForbiddenError               403 Forbidden
        APINotFoundError                404 Not Found
        APIMethodNotAllowed             405 Method Not Allowed
        APINotAcceptableError           406 Not Acceptable
        APIConflictError                409 Conflict
        APIGoneError                    410 Gone
        APIUnsupportedMediaTypeError    415 Unsupported Media Type
        APIAuthenticationTimeoutError   419 Authentication Timeout
        APITooManyRequestsError         429 Too Many Requests
        APIInternalServerError          500 Internal Server Error
        APINotImplementedError          501 Not Implemented
        APIUnavailableError             503 Service Unavailable

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
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request.",
                 **kwargs):
        """
        APIError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APIError, self).__init__(code=code, message=message, title=title, **kwargs)


class APIBadRequestError(APIError):
    """Convenience class for HTTP 400 errors"""

    def __init__(self,
                 code="400",
                 title="Bad Request",
                 message="The request could not be understood by the server due to malformed syntax.",
                 **kwargs):
        """
        APIBadRequestError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APIBadRequestError, self).__init__(code=code, title=title, message=message, **kwargs)


class APIUnauthorizedError(APIError):
    """Convenience class for HTTP 401 errors"""

    def __init__(self,
                 code="401",
                 title="Unauthorized",
                 message="The request requires user authentication.",
                 **kwargs):
        """
        APIUnauthorizedError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APIUnauthorizedError, self).__init__(code=code, title=title, message=message, **kwargs)


class APIForbiddenError(APIError):
    """Convenience class for HTTP 403 errors"""

    def __init__(self,
                 code="403",
                 title="Forbidden",
                 message="The server understood the request, but is refusing to fulfill it.",
                 **kwargs):
        """
        APIForbiddenError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APIForbiddenError, self).__init__(code=code, title=title, message=message, **kwargs)


class APINotFoundError(APIError):
    """Convenience class for HTTP 404 errors"""

    def __init__(self,
                 code="404",
                 title="Not Found",
                 message="The server could not find the requested resource.",
                 **kwargs):
        """
        APINotFoundError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APINotFoundError, self).__init__(code=code, title=title, message=message, **kwargs)


class APIMethodNotAllowedError(APIError):
    """Convenience class for HTTP 405 errors"""

    def __init__(self,
                 code="405",
                 title="Method Not Allowed",
                 message="The HTTP method specified in the request is not allowed for the requested resource.",
                 **kwargs):
        """
        APIMethodNotAllowedError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APIMethodNotAllowedError, self).__init__(code=code, title=title, message=message, **kwargs)


class APINotAcceptableError(APIError):
    """Convenience class for HTTP 406 errors"""

    def __init__(self,
                 code="406",
                 title="Not Acceptable",
                 message="The requested resource cannot generate content deemed acceptable by the request.",
                 **kwargs):
        """
        APINotAcceptableError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APINotAcceptableError, self).__init__(code=code, title=title, message=message, **kwargs)


class APIConflictError(APIError):
    """Convenience class for HTTP 409 errors"""

    def __init__(self,
                 code="409",
                 title="Conflict",
                 message="The request could not be completed due to a conflict with the current state of the resource.",
                 **kwargs):
        """
        APIConflictError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APIConflictError, self).__init__(code=code, title=title, message=message, **kwargs)


class APIGoneError(APIError):
    """Convenience class for HTTP 410 errors"""

    def __init__(self,
                 code="410",
                 title="Gone",
                 message="The requested resource is no longer available and no forwarding address is known.",
                 **kwargs):
        """
        APIGoneError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APIGoneError, self).__init__(code=code, title=title, message=message, **kwargs)


class APIUnsupportableMediaTypeError(APIError):
    """Convenience class for HTTP 415 errors"""

    def __init__(self,
                 code="415",
                 title="Unsupportable Media Type",
                 message="The content supplied in the request is not a type supported by the requested resource.",
                 **kwargs):
        """
        APIUnsupportableMediaTypeError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APIUnsupportableMediaTypeError, self).__init__(code=code, title=title, message=message, **kwargs)


class APIAuthenticationTimeoutError(APIError):
    """Convenience class for HTTP 419 errors"""

    def __init__(self,
                 code="419",
                 title="Authentication Timeout",
                 message="Previously valid authentication has expired. Please re-authenticate and try again.",
                 **kwargs):
        """
        APIAuthenticationTimeoutError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APIAuthenticationTimeoutError, self).__init__(code=code, title=title, message=message, **kwargs)


class APITooManyRequestsError(APIError):
    """Convenience class for HTTP 429 errors"""

    def __init__(self,
                 code="429",
                 title="Too Many Requests",
                 message="The server is temporarily refusing to service requests made by the client " +
                         "due to too many requests being made by the client too frequently.",
                 **kwargs):
        """
        APITooManyRequestsError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APITooManyRequestsError, self).__init__(code=code, title=title, message=message, **kwargs)


class APIInternalServerError(APIError):
    """Convenience class for HTTP 500 errors"""

    def __init__(self,
                 code="500",
                 title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request.",
                 **kwargs):
        """
        APIInternalServerError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APIInternalServerError, self).__init__(code=code, title=title, message=message, **kwargs)


class APINotImplementedError(APIError):
    """Convenience class for HTTP 501 errors"""

    def __init__(self,
                 code="501",
                 title="Not Implemented",
                 message="The server does not support the functionality required to fulfill the request.",
                 **kwargs):
        """
        APINotImplementedError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APINotImplementedError, self).__init__(code=code, title=title, message=message, **kwargs)


class APIServiceUnavailableError(APIError):
    """Convenience class for HTTP 503 errors"""

    def __init__(self,
                 code="503",
                 title="Service Unavailable",
                 message="The server is currently unable to handle the request due to a temporary " +
                         "overloading or maintenance of the server.",
                 **kwargs):
        """
        APIServiceUnavailableError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :param kwargs: Other nonstandard error information
        :return:
        """
        super(APIServiceUnavailableError, self).__init__(code=code, title=title, message=message, **kwargs)


class Contact(ABC):
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
        super(Contact, self).__init__(db, blackbook.couch.models.Contact)

    def _generate_document(self, *args, **kwargs):
        """Generate a Contact document representation."""

        document = collection_plus_json.Collection(href=self.api_spec["endpoint"])
        return document

    def delete(self, *args, **kwargs):
        pass

    def get(self, contact_id=None, user_id=None):

        user_api = User(self.db)
        session_api = Session(self.db)

        user = self._get_authenticated_user(user_api, session_api)
        document = self._generate_document()
        spec_properties = self.api_spec["properties"]

        if not self._request_origin_consistent():
            # TODO: handle bad CSRF
            pass

        if not user:
            document.error = APIUnauthorizedError()
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
                document.error = APINotFoundError()
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
                    document.error = APINotFoundError()
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
                    document.error = APINotFoundError()
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

    def patch(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        pass


class Session(ABC):
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
        super(Session, self).__init__(db, blackbook.couch.models.Session)

    def _generate_document(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        pass

    def patch(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        pass


class User(ABC):
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
        super(User, self).__init__(db, blackbook.couch.models.User)

    def _generate_document(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
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

    database = blackbook.couch.database.init_db(app)

    api_blueprint = Blueprint("api", __name__, url_prefix="/api")

    contact_view = Contact(database).as_view('contact_api')
    api_blueprint.add_url_rule('/contact/', defaults={'user_id': None}, view_func=contact_view, methods=["GET", "POST"])
    api_blueprint.add_url_rule('/contact/<contact_id>/', defaults={'user_id': None, 'contact_id': None},
                               view_func=contact_view, methods=["GET", "PATCH", "PUT", "DELETE"])
    api_blueprint.add_url_rule('/user/<user_id>/contacts/', defaults={'user_id': None},
                               view_func=contact_view, methods=["GET", "POST"])

    return api_blueprint