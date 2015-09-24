from blackbook.lib import collection_plus_json

__author__ = 'ievans3024'


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