import blackbook.lib.collection_plus_json as collection_json
from blackbook.database import Contact, Permission, Session, User
from datetime import datetime
from flask.views import MethodView
from flask import session, request, Response, current_app
from werkzeug import security

__author__ = 'ievans3024'


class APIError(BaseException):
    """
    Wrapper class for API Errors

    May be raised as a python exception, i.e.:
        raise APIError()

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
        self.code = code
        self.message = message
        self.title = title
        super(APIError, self).__init__(**kwargs)

    def __str__(self):
        return 'HTTP {0} {1}: {2}'.format(self.code, self.title, self.message)


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


class API(MethodView):

    def __init__(self, app, db, endpoint_root):
        self.app = app
        self.db = db
        self.endpoint_root = endpoint_root
        super(API, self).__init__()

    def _generate_document(self, *args, **kwargs):
        document = collection_json.Collection(href=self.endpoint_root)
        return document

    def _error(self, error):
        document = self._generate_document()
        document.error = collection_json.Error(code=error.code, title=error.title, message=error.message)
        return error.code, str(document)

    def _session_ok(self):
        # get session id and token from cookies
        # get session from database
        #   if not exists, raise APINotFoundError
        # ensure session is unexpired
        #   if expired, delete from db and raise APIAuthenticationTimeoutError
        pass

    def _user_by_session(self):
        # call _session_ok
        # allow errors to bubble
        # get user by session
        # return user model instance
        pass


class ContactAPI(API):

    def delete(self, contact_id):
        return 'Contact API - DELETE'

    def _generate_document(self, model_instance=None):
        document = super(ContactAPI, self)._generate_document()
        # add endpoint specific features (template, queries, etc.)
        # read model instance values and put them in document.items
        #
        return document

    def get(self, contact_id=None):
        document = self._generate_document()
        if contact_id is not None:
            data_array = collection_json.Array([], cls=collection_json.Data)
            data = collection_json.Data(name='id', prompt='ID Number', value=contact_id)
            data_array.append(data)
            item = collection_json.Item(href=request.path, data=data_array)
            document.items = collection_json.Array([], cls=collection_json.Item)
            document.items.append(item)
        return Response(response=str(document), mimetype=document.mimetype)

    def head(self, contact_id=None):
        return ''

    def patch(self, contact_id):
        return 'Contact API - PATCH'

    def post(self):
        return 'Contact API - POST'


class SessionAPI(API):

    def delete(self):
        # call _session_ok
        # catch errors and return _error code
        # remove from db and return 200 OK if no errors raise
        pass

    def _generate_document(self, model_instance=None):
        pass

    def get(self):
        return self.head()

    def head(self):
        # call _session_ok
        # catch errors and return _error code
        # return 200 OK without body if no errors raise
        pass

    def patch(self):
        # call _session_ok
        # catch errors and return _error code
        # update session expiry
        # return 200 OK without body if no errors raise
        pass

    def post(self):
        # get user from posted credentials
        # return 400 Bad Request if credential failure
        # generate session token
        # create session in database
        # return 200 OK with body containing session token
        pass


class UserAPI(API):

    def delete(self):
        pass

    def _generate_document(self, model_instance=None):
        pass

    def get(self):
        pass

    def head(self):
        pass

    def patch(self):
        pass

    def post(self):

        def create_root_user(app, name, email, password, contact_info=None):

            contact_info = Contact(date_created=datetime.now(), date_modified=datetime.now(), name_prefix='',
                                   name_first='', name_middle='', name_last='', name_suffix='', addresses=[], emails=[],
                                   phone_numbers=[])
            current_app.db.session.add(contact_info)
            current_app.db.session.commit()
            permissions = [p.permission for p in Permission.query.all()]
            password_hash = security.generate_password_hash(password,
                                                            method=app.config.get('BLACKBOOK_PASSWORD_HASH_METHOD'),
                                                            salt_length=app.config.get(
                                                                'BLACKBOOK_PASSWORD_SALT_LENGTH'))
            root = User(date_created=datetime.now(), date_modified=datetime.now(), email=email,
                        password_hash=password_hash, display_name=name, permissions=permissions,
                        contact_info=contact_info.id)
            current_app.db.session.add(root)
            current_app.db.session.commit()
        # get user session, if existent
        # user must have permission to create accounts
        # validate form
        users = User.query.all()
        # first user created will be "root"
        if not len(users):
            create_root_user(current_app, '', '', '')
        else:
            # handle public registration if not user session and users exist
            pass
        # user must have permission to create admins if admin permissions are supplied

        # create User
        # attempt commit
        # catch errors and handle appropriately
        # return created user in document
        pass
