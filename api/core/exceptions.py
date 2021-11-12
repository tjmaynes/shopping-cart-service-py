class CustomException(Exception):
    """Basic exception for errors raised"""

class DBConnectionFailedException(CustomException):
    """Unable to connect to repository"""

class NotFoundException(CustomException):
    """Unable to find item in repository"""

class InvalidItemException(CustomException):
    """Given an invalid item"""

class BadRequestException(CustomException):
    """Invalid item given"""

class UnknownException(CustomException):
    """Unknown"""