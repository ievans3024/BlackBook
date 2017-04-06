import blackbook.lib.collection_plus_json as collection_json
from blackbook.database import Contact, Permission, Session, User
from datetime import datetime
from flask.views import MethodView
from flask import session, request, Response, current_app
from werkzeug import security

__author__ = 'ievans3024'


class APIError(Exception):
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
                 endpoint=None,
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
        self.endpoint = endpoint
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

    @staticmethod
    def _get_session():
        token = session.get('token')

        if token is None:
            return None

        user_session = Session.query.filter_by(token=token)

        if not len(user_session):
            raise APIUnauthorizedError()

        if user_session.expiry <= datetime.now():
            current_app.db.session.delete(user_session)
            current_app.db.commit()
            raise APIAuthenticationTimeoutError()

        return user_session

    def _get_session_user(self):
        user_session = self._get_session()

        if user_session is None:
            return None

        user = User.query.filter_by(id=user_session.session_user).first()

        if not user:
            return None

        return user


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

    def _generate_document(self, *model_instances):

        document = super(UserAPI, self)._generate_document()
        session_user = self._get_session_user()

        if len(model_instances):
            for instance in model_instances:
                href = self.endpoint_root + str(instance.id)

                # direct user properties
                data = collection_json.Array([], collection_json.Data)
                data.append(collection_json.Data(name='email', prompt='Email', value=instance.email))
                data.append(collection_json.Data(name='name', prompt='Name', value=instance.name))
                if session_user is not None and session_user.has_permission('blackbook.user.edit.other'):
                    for p in instance.permissions:
                        d = collection_json.Data(name='permission', prompt='Permissions', value=p.permission)
                        data.append(d)

                # relational user properties (contacts, contact info, etc.)
                links = collection_json.Array([], collection_json.Link)

                document.items.append(collection_json.Item(href, data, links))

        return document

    def get(self, user_id=None):

        session_user = self._get_session_user()

        if session_user is None:
            raise APIUnauthorizedError(endpoint=self.endpoint_root)

        if user_id is not None:
            if (user_id == session_user.id) or (session_user.has_permission('blackbook.user.read.other')):
                user = User.query.filter_by(id=user_id).first()
                if not user:
                    raise APINotFoundError(endpoint=self.endpoint_root)
                document = self._generate_document(user)
                return Response(response=str(document), mimetype=document.mimetype)

        if session_user.has_permission('blackbook.user.read.other'):
            users = User.query.all()
            # TODO: pagination
            document = self._generate_document(*users)
            return Response(response=str(document), mimetype=document.mimetype)

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
            return root
        # validate form

        # first user created will be "root"
        users = User.query.all()
        if not len(users):
            root = create_root_user(current_app, '', '', '')
            response = self._generate_document(root)
            return Response(response=str(response), mimetype=response.mimetype)

        if not current_app.config.get('BLACKBOOK_PUBLIC_REGISTRATION'):

            user = self._get_session_user().first()

            if len(user):

                user = user.first()

                # user must have permission to create accounts
                can_create_users = user.has_permission('blackbook.user.create')
                if not can_create_users:
                    raise APIForbiddenError()

                # user must have permission to edit other users if permissions are supplied
                can_edit_permissions = user.has_permission('blackbook.user.edit.other')
                if len(request.form.getlist('permissions')) and not can_edit_permissions:
                    raise APIForbiddenError()

                # user must have permission to edit admins if admin permissions are supplied
                has_admin_permissions = user.has_permission('blackbook.admin.edit')
                admin_permissions_supplied = [
                    p
                    for p in request.form.getlist('permissions')
                    if p.startswith('blackbook.admin')
                ]
                if len(admin_permissions_supplied) and not has_admin_permissions:
                    raise APIForbiddenError()

        # create User
        # attempt commit
        # catch errors and handle appropriately
        # return created user in document
        pass
