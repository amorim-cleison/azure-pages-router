
class InvalidPathError(ValueError):
    pass


class MissingArgumentError(ValueError):
    pass


class RouteNotFoundError(Exception):
    pass


class InternalServerError(Exception):
    pass
