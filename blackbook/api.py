from .lib import collection_plus_json as collection_json
from .database import Contact, Permission, Session, User, user_contacts
from datetime import datetime, timedelta
from flask.views import MethodView
from flask import request, Response, current_app
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug import security

__author__ = 'ievans3024'

jwt = JWT(current_app)


@jwt.authentication_handler
def jwt_auth(username, password):
    user = User.query.filter_by(email=username).first()
    if user and security.check_password_hash(user.password_hash, password):
        now = datetime.now()
        lifetime = current_app.config.get('JWT_EXPIRATION_DELTA')
        expiry = now + lifetime
        session = Session(date_created=now, date_modified=now, expiry=expiry)
        current_app.db.session.add(session)
        current_app.db.commit()
        return session


@jwt.identity_handler
def jwt_identity(payload):
    session_id = payload['session_id']
    session = Session.query.get(session_id)
    if session is None:
        raise APIUnauthorizedError()
    elif session.expiry > datetime.now():
        current_app.db.session.delete(session)
        current_app.db.commit()
        raise APIAuthenticationTimeoutError()
    else:
        return session


@jwt.jwt_payload_handler
def jwt_payload(identity):
    return {'session_id': identity.id}


@jwt.jwt_error_handler
def jwt_error(error):
    if isinstance(error, APIError):
        raise error
    else:
        raise APIInternalServerError(
            message='An error occurred while validating session information.',
            endpoint=request.path
        )


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


class ContactAPI(API):

    @jwt_required
    def delete(self, contact_id):
        return 'Contact API - DELETE'

    def _generate_document(self, model_instance=None):
        document = super(ContactAPI, self)._generate_document()
        # add endpoint specific features (template, queries, etc.)
        # read model instance values and put them in document.items
        #
        return document

    @jwt_required
    def get(self, contact_id=None):

        document = self._generate_document()

        if contact_id is not None:
            contact = Contact.query.get(contact_id)

            if contact is None:
                raise APINotFoundError()

            # get is contact owner or has permission to see others' contacts

            if (
                (not current_identity.user.contact_info.id == contact.id) or
                (not user_contacts.select(User, Contact).where(
                    User.id == current_identity.user.id and Contact.id == contact.id)) or
                (not current_identity.user.has_permission('blackbook.contact.read.other'))
            ):
                raise APIForbiddenError()
        else:
            for contact in current_identity.user.contacts:
                href = '/'.join([request.path, contact.id, ''])
                item = {
                    'href': href,
                    'data': [
                        {'name': 'name_prefix', 'prompt': 'Prefix', 'hint': 'Dr.', 'value': contact.name_prefix},
                        {'name': 'name_first', 'prompt': 'First Name', 'hint': 'Seymour', 'value': contact.name_first},
                        {
                            'name': 'name_middle',
                            'prompt': 'Middle Name',
                            'hint': 'Gluteus',
                            'value': contact.name_middle
                        },
                        {'name': 'name_last', 'prompt': 'Last Name', 'hint': 'Maximus', 'value': contact.name_last},
                        {'name': 'name_suffix', 'prompt': 'Suffix', 'hint': 'III', 'value': contact.name_suffix}
                    ],
                    'links': [
                        {'href': href + '/addresses/', 'rel': 'more', 'name': 'addresses', 'prompt': 'Addresses'},
                        {'href': href + '/emails/', 'rel': 'more', 'name': 'emails', 'prompt': 'Emails'},
                        {
                            'href': href + '/phone-numbers/',
                            'rel': 'more',
                            'name': 'phone_numbers',
                            'prompt': 'Phone Numbers'
                        }
                    ]
                }
                document.items.append(collection_json.Item(**item))
        return Response(response=str(document), mimetype=document.mimetype)

    @jwt_required
    def head(self, contact_id=None):
        return ''

    @jwt_required
    def patch(self, contact_id):
        return 'Contact API - PATCH'

    @jwt_required
    def post(self):
        return 'Contact API - POST'


class SessionAPI(API):

    @jwt_required
    def delete(self):
        if current_identity is not None:
            current_app.db.session.delete(current_identity)
            current_app.db.commit()
            return '', 200
        else:
            raise APIBadRequestError()

    def _generate_document(self, model_instance=None):
        document = super(SessionAPI, self)._generate_document(model_instance=model_instance)
        template = {
            'data': [
                {'name': 'email', 'prompt': 'Email', 'hint': 'user@example.com', 'type': 'text'},
                {'name': 'password', 'prompt': 'Password', 'hint': None, 'type': 'password'}
            ]
        }
        document.template = collection_json.Template(**template)
        return document

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

    @jwt_required
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

    @jwt_required
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
                if session_user is not None and session_user.has_permission('blackbook.user.edit'):
                    for p in instance.permissions:
                        d = collection_json.Data(name='permission', prompt='Permissions', value=p.permission)
                        data.append(d)

                # relational user properties (contacts, contact info, etc.)
                links = collection_json.Array([], collection_json.Link)

                document.items.append(collection_json.Item(href, data, links))

        return document

    def _create_user(self):
        pass

    def _create_user_public(self):
        pass

    @jwt_required
    def _create_user_protected(self):

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

    @jwt_required
    def get(self, user_id=None):

        session_user = self._get_session_user()

        if session_user is None:
            raise APIUnauthorizedError(endpoint=self.endpoint_root)

        if user_id is not None:
            if (user_id == session_user.id) or (session_user.has_permission('blackbook.user.read')):
                user = User.query.filter_by(id=user_id).first()
                if not user:
                    raise APINotFoundError(endpoint=self.endpoint_root)
                document = self._generate_document(user)
                return Response(response=str(document), mimetype=document.mimetype)

        if session_user.has_permission('blackbook.user.read'):
            users = User.query.all()
            # TODO: pagination
            document = self._generate_document(*users)
            return Response(response=str(document), mimetype=document.mimetype)

    @jwt_required
    def head(self):
        pass

    @jwt_required
    def patch(self):
        pass

    def post(self):
        # validate form

        if not current_app.config.get('BLACKBOOK_PUBLIC_REGISTRATION'):

            return self._create_user_protected()

        else:

            return self._create_user_protected()

        # create User
        # attempt commit
        # catch errors and handle appropriately
        # return created user in document
        pass
