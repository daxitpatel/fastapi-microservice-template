from builtins import Exception

__all__ = ["WotnotException", "BadMessageErrorException", "InternalServerException", "BadRequestError"]


class WotnotException(Exception):
    pass


class BadMessageErrorException(WotnotException):
    pass


class InternalServerException(WotnotException):
    pass


class BadRequestError(WotnotException):
    pass
