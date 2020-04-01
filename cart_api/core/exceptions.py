class RepositoryException(Exception):
    """Basic exception for errors raised by a repository"""

class ConnectionFailedRepositoryException(RepositoryException):
    """Unable to connect to repository"""

class NotFoundRepositoryException(RepositoryException):
    """Unable to find item in repository"""


class ServiceException(Exception):
    """Basic exception for errors raised by a service"""

class BadRequestServiceException(ServiceException):
    """Nothing returned from the repository"""

class InvalidItemException(Exception):
    """Given an invalid item"""

class UnknownException(ServiceException, RepositoryException):
    """Unknown"""