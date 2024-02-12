from .errors import *

PAGE_DEFAULT_ERROR = "pages/error.html"


class ErrorHandler:
    def __init__(self, status, status_code, exceptions, page=PAGE_DEFAULT_ERROR):
        self.status = status
        self.status_code = status_code
        self.exceptions = exceptions
        self.page = page


# HTTP codes x error handlers:
HTTP_CODES_HANDLERS = [
    ErrorHandler(
        status="Bad request",
        status_code=400,
        exceptions=[MissingArgumentError, InvalidPathError]
    ),
    ErrorHandler(
        status="Not found",
        status_code=404,
        exceptions=[RouteNotFoundError]
    ),
    ErrorHandler(
        status="Internal server error",
        status_code=500,
        exceptions=[InternalServerError]
    )
]
