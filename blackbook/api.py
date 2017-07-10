from database import JSONObject, Contact, Permission, Session, User
from datetime import datetime, timedelta
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

    def __init__(self, *args, code="500", title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request.", endpoint=None):
        """
        APIError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :return:
        """
        self.code = code
        self.message = message
        self.title = title
        self.endpoint = endpoint
        super(APIError, self).__init__(*args)

    def __str__(self):
        return 'HTTP {0} {1}: {2}'.format(self.code, self.title, self.message)

    @property
    def serializable(self):
        return self.__dict__


class APIBadRequestError(APIError):
    """Convenience class for HTTP 400 errors"""

    def __init__(self, *args, code="500", title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request."):
        """
        APIBadRequestError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :return:
        """
        super(APIBadRequestError, self).__init__(*args, code=code, title=title, message=message)


class APIUnauthorizedError(APIError):
    """Convenience class for HTTP 401 errors"""

    def __init__(self, *args, code="500", title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request."):
        """
        APIUnauthorizedError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :return:
        """
        super(APIUnauthorizedError, self).__init__(*args, code=code, title=title, message=message)


class APIForbiddenError(APIError):
    """Convenience class for HTTP 403 errors"""

    def __init__(self, *args, code="500", title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request."):
        """
        APIForbiddenError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :return:
        """
        super(APIForbiddenError, self).__init__(*args, code=code, title=title, message=message)


class APINotFoundError(APIError):
    """Convenience class for HTTP 404 errors"""

    def __init__(self, *args, code="500", title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request."):
        """
        APINotFoundError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :return:
        """
        super(APINotFoundError, self).__init__(*args, code=code, title=title, message=message)


class APIMethodNotAllowedError(APIError):
    """Convenience class for HTTP 405 errors"""

    def __init__(self, *args, code="500", title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request."):
        """
        APIMethodNotAllowedError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :return:
        """
        super(APIMethodNotAllowedError, self).__init__(*args, code=code, title=title, message=message)


class APINotAcceptableError(APIError):
    """Convenience class for HTTP 406 errors"""

    def __init__(self, *args, code="500", title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request."):
        """
        APINotAcceptableError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :return:
        """
        super(APINotAcceptableError, self).__init__(*args, code=code, title=title, message=message)


class APIConflictError(APIError):
    """Convenience class for HTTP 409 errors"""

    def __init__(self, *args, code="500", title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request."):
        """
        APIConflictError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :return:
        """
        super(APIConflictError, self).__init__(*args, code=code, title=title, message=message)


class APIGoneError(APIError):
    """Convenience class for HTTP 410 errors"""

    def __init__(self, *args, code="500", title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request."):
        """
        APIGoneError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :return:
        """
        super(APIGoneError, self).__init__(*args, code=code, title=title, message=message)


class APIUnsupportableMediaTypeError(APIError):
    """Convenience class for HTTP 415 errors"""

    def __init__(self, *args, code="500", title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request."):
        """
        APIUnsupportableMediaTypeError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :return:
        """
        super(APIUnsupportableMediaTypeError, self).__init__(*args, code=code, title=title, message=message)


class APIAuthenticationTimeoutError(APIError):
    """Convenience class for HTTP 419 errors"""

    def __init__(self, *args, code="500", title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request."):
        """
        APIAuthenticationTimeoutError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :return:
        """
        super(APIAuthenticationTimeoutError, self).__init__(*args, code=code, title=title, message=message)


class APITooManyRequestsError(APIError):
    """Convenience class for HTTP 429 errors"""

    def __init__(self, *args, code="500", title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request."):
        """
        APITooManyRequestsError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :return:
        """
        super(APITooManyRequestsError, self).__init__(*args, code=code, title=title, message=message)


class APIInternalServerError(APIError):
    """Convenience class for HTTP 500 errors"""

    def __init__(self, *args, code="500", title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request."):
        """
        APIInternalServerError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :return:
        """
        super(APIInternalServerError, self).__init__(*args, code=code, title=title, message=message)


class APINotImplementedError(APIError):
    """Convenience class for HTTP 501 errors"""

    def __init__(self, *args, code="500", title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request."):
        """
        APINotImplementedError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :return:
        """
        super(APINotImplementedError, self).__init__(*args, code=code, title=title, message=message)


class APIServiceUnavailableError(APIError):
    """Convenience class for HTTP 503 errors"""

    def __init__(self, *args, code="500", title="Internal Server Error",
                 message="The server encountered an unexpected condition which prevented it from " +
                         "fulfilling the request."):
        """
        APIServiceUnavailableError Constructor
        :param code: The HTTP error code
        :param title: The title of the error
        :param message: The detailed error description
        :return:
        """
        super(APIServiceUnavailableError, self).__init__(*args, code=code, title=title, message=message)


class API(MethodView):
    def __init__(self, app, db, endpoint_root):
        self.app = app
        self.db = db
        self.endpoint_root = endpoint_root
        super(API, self).__init__()

    def _generate_document(self, *args, **kwargs):
        return JSONObject(**kwargs)

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
    forms = {
        'create': [
            {'label': 'Prefix', 'type': 'text', 'name': 'prefix', 'hint': 'Dr., Mr., Mrs.',
             'required': False},
            {'label': 'First Name', 'type': 'text', 'name': 'name_first', 'hint': None, 'required': True},
            {'label': 'Middle Name', 'type': 'text', 'name': 'name_middle', 'hint': None, 'required': False},
            {'label': 'Last Name', 'type': 'text', 'name': 'name_last', 'hint': None, 'required': False},
            {'label': 'Suffix', 'type': 'text', 'name': 'suffix', 'hint': 'Jr., II, III, Esq.',
             'required': False},
            {
                'label': 'Addresses',
                'type': 'array',
                'name': 'addresses',
                'template': [
                    {'label': 'Label', 'type': 'text', 'name': 'label', 'hint': 'Home, Work, Office',
                     'required': False},
                    {'label': 'Company', 'type': 'text', 'name': 'company', 'hint': None, 'required': False},
                    {'label': 'Name', 'type': 'text', 'name': 'name', 'hint': None, 'required': False},
                    {'label': 'Street', 'type': 'text', 'name': 'street', 'hint': '123 Example St.',
                     'required': True},
                    {'label': 'Unit', 'type': 'text', 'name': 'unit', 'hint': None, 'required': False},
                    {'label': 'City', 'type': 'text', 'name': 'city', 'hint': 'Exampleton', 'required': True},
                    {'label': 'Locality', 'type': 'text', 'name': 'locality', 'hint': 'EX', 'required': True},
                    {'label': 'Postal Code', 'type': 'text', 'name': 'postal_code', 'hint': '12345',
                     'required': True},
                    {'label': 'Country', 'type': 'text', 'name': 'country', 'hint': None, 'required': False}
                ]
            },
            {
                'label': 'Emails',
                'type': 'array',
                'name': 'emails',
                'template': [
                    {'label': 'Label', 'type': 'text', 'name': 'label', 'hint': 'Home, Work, Office',
                     'required': False},
                    {'label': 'Email', 'type': 'text', 'name': 'address', 'hint': None, 'required': True}
                ]
            },
            {
                'label': 'Phone numbers',
                'type': 'array',
                'name': 'phone_numbers',
                'template': [
                    {'label': 'Label', 'type': 'text', 'name': 'label', 'hint': 'Home, Work, Office',
                     'required': False},
                    {'label': 'Phone Number', 'type': 'text', 'name': 'number', 'hint': None, 'required': True}
                ]
            }

        ]
    }

    def delete(self, contact_id):
        return 'Contact API - DELETE'

    def _generate_document(self, *model_instances, **doc_props):
        opts = dict(
            {
                'data': [m.public_document for m in model_instances],
                'forms': {}
            },
            **doc_props
        )
        if not len(model_instances):
            form_key = 'create'
        else:
            form_key = 'update'
        opts['forms'][form_key] = self.forms['create']
        return JSONObject(**opts)

    def get(self, contact_id=None):
        session_user = self._get_session_user()
        response = self.head(contact_id=contact_id)
        # if self.head() raises any errors, this should be unreachable
        if contact_id is not None:
            contact = Contact.query.get(contact_id)
            document = self._generate_document(contact)
        else:
            document = self._generate_document(*session_user.contacts)
        return Response(response=str(document), status=response.status_code, mimetype=document.mimetype)

    def head(self, contact_id=None):
        session_user = self._get_session_user()
        if session_user is None:
            raise APIUnauthorizedError()
        else:
            if contact_id is not None:
                c = Contact.query.get(contact_id)
                if not c:
                    raise APINotFoundError()
            return Response(response='', status=200, mimetype=JSONObject.mimetype)

    def patch(self, contact_id):
        return 'Contact API - PATCH'

    def post(self):
        return 'Contact API - POST'


class SessionAPI(API):
    forms = {
        'create': [
            {'label': 'Email', 'type': 'text', 'name': 'email', 'hint': 'username@example.com', 'required': True},
            {'label': 'Password', 'type': 'password', 'name': 'password', 'hint': None, 'required': True}
        ]
    }

    def delete(self):
        user_session = self._get_session()
        if user_session is not None:
            current_app.db.session.delete(user_session)
            current_app.db.commit()
            return '', 200
        else:
            raise APIBadRequestError()

    def _generate_document(self, *model_instances, **doc_props):
        opts = dict(
            {
                'data': [m.public_document for m in model_instances]
            },
            **doc_props
        )
        if not len(model_instances):
            opts['forms'] = self.forms
        return super(SessionAPI, self)._generate_document(**opts)

    def get(self):
        user_session = self._get_session()
        if user_session is not None:
            return Response(response='', status=200, mimetype=JSONObject.mimetype)
        else:
            document = self._generate_document(user_session)
            return Response(response=str(document), status=401, mimetype=document.mimetype)

    def head(self):
        user_session = self._get_session()
        if user_session is not None:
            return Response(response='', status=200, mimetype=JSONObject.mimetype)
        else:
            raise APIUnauthorizedError()

    def patch(self):
        user_session = self._get_session()
        if user_session is not None:
            user_session.expiry = datetime.now() + current_app.config.get('PERMANENT_SESSION_LIFETIME')
            current_app.db.session.add(user_session)
            current_app.db.session.commit()
            return Response(response='', status=200, mimetype=JSONObject.mimetype)
        else:
            raise APIBadRequestError()

    def post(self):
        user = User.query.filter_by(email=request.form.get('email'))

        if not user:
            raise APIBadRequestError(message='Incorrect credentials')

        if not security.check_password_hash(user.password_hash, request.form.get('password')):
            raise APIBadRequestError(message='Incorrect credentials')

        # get user from posted credentials
        # return 400 Bad Request if credential failure
        # generate session token
        # create session in database
        # return 200 OK with body containing session token
        pass


class UserAPI(API):
    forms = {
        'create': [
            {'label': 'Display Name', 'type': 'text', 'name': 'display_name',
             'hint': 'A cosmetic display name to identify yourself.'},
            {'label': 'Email', 'type': 'text', 'name': 'email', 'hint': 'username@example.com'},
            {'label': 'Password', 'type': 'password', 'name': 'password', 'hint': None}
        ],
        'update': [
            {'label': 'Display Name', 'type': 'text', 'name': 'display_name',
             'hint': 'A cosmetic display name to identify yourself.'},
            {'label': 'Email', 'type': 'text', 'name': 'email', 'hint': 'username@example.com'},
            {
                'label': 'Contact Info',
                'type': 'object',
                'name': 'contact_info',
                'template': ContactAPI.forms['create']
            },
            {
                'label': 'Contacts',
                'type': 'array',
                'name': 'contacts',
                'template': ContactAPI.forms['create']
            }
        ],
        'change_password': [
            {'label': 'Current Password', 'type': 'password', 'name': 'old_password', 'hint': None},
            {'label': 'New Password', 'type': 'password', 'name': 'new_password', 'hint': None}
        ]
    }

    def delete(self):
        pass

    def _generate_document(self, *model_instances, **doc_props):

        opts = {
            'data': [m.public_document for m in model_instances],
            'forms': {}
        }
        if not len(model_instances):
            opts['forms']['create'] = self.forms['create']
        else:
            opts['forms']['update'] = self.forms['update']
            opts['forms']['change_password'] = self.forms['change_password']

        return super(UserAPI, self)._generate_document(**opts)

    def get(self, user_id=None):

        session_user = self._get_session_user()

        if session_user is None:
            raise APIUnauthorizedError()

        if user_id is not None:
            if (user_id == session_user.id) or (session_user.has_permission('blackbook.user.read')):
                user = User.query.filter_by(id=user_id).first()
                if not user:
                    raise APINotFoundError()
                document = self._generate_document(user)
                return Response(response=str(document), status=200, mimetype=document.mimetype)

        if session_user.has_permission('blackbook.user.read'):
            users = User.query.all()
            # TODO: pagination
            document = self._generate_document(*users)
            return Response(response=str(document), mimetype=document.mimetype)

    def head(self):
        pass

    def patch(self):
        pass

    def post(self):
        # validate form

        if not current_app.config.get('BLACKBOOK_PUBLIC_REGISTRATION'):

            user = self._get_session_user().first()

            if len(user):

                user = user.first()

                # user must have permission to create accounts
                can_create_users = user.has_permission('blackbook.user.create')
                if not can_create_users:
                    raise APIForbiddenError()

                # user must have permission to edit other users if permissions are supplied
                can_edit_permissions = user.has_permission('blackbook.user.edit')
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
