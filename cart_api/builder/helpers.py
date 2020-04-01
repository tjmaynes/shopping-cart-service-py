from flask import Response, jsonify
from typing import TypeVar
from cart_api.core.exceptions import RepositoryException, NotFoundRepositoryException, BadRequestServiceException


T = TypeVar("T")


def map_exception_to_status(exception: Exception) -> int:
    try:
        raise exception
    except BadRequestServiceException:
        return 422
    except NotFoundRepositoryException:
        return 404
    except:
        return 500


def handle_success(item: T, status: int = 200):
    return jsonify(item), status


def handle_exception(exception) -> Response:
    return jsonify(exception.args), map_exception_to_status(exception)