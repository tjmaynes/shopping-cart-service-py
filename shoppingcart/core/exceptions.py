class CustomException(Exception):
    """Basic exception for errors raised"""

    def __init__(self, message=""):
        self.message = message

    def __str__(self):
        return self.message

    pass


class DBConnectionFailedException(CustomException):
    """Unable to connect to repository"""

    pass


class NotFoundException(CustomException):
    """Unable to find item in repository"""

    pass


class InvalidItemException(CustomException):
    """Given an invalid item"""

    pass


class BadRequestException(CustomException):
    """Invalid item given"""

    pass


class UnknownException(CustomException):
    """Unknown"""

    pass
