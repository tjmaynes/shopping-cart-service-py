from typing import List, Callable, TypeVar, Generic, Dict
from .repository import Repository
from .exceptions import ServiceException, UnknownException, InvalidItemException, BadRequestServiceException
import python_either.either as E


T = TypeVar("T")


class Service(Generic[T]):
    def __init__(self, repository: Repository, validate_item: Callable[[Dict[str, str]], E.Either[T, Exception]]):
        self.__repository = repository
        self.__validate_item = validate_item

    def __handle_exception(self, exception: Exception) -> ServiceException:
        return BadRequestServiceException(exception.args) if exception == InvalidItemException else exception

    def get_items(self, page_number: int = 0, page_size: int = 10) -> E.Either[List[T], ServiceException]:
        return self.__repository.get_all_items(page_number=page_number, page_size=page_size) | E.map_error | self.__handle_exception
        
    def get_item_by_id(self, id: str) -> E.Either[T, ServiceException]:
        return self.__repository.get_item_by_id(id) | E.map_error | self.__handle_exception

    def add_item(self, item: Dict[str, str]) -> E.Either[T, ServiceException]:
        return self.__validate_item(item) \
            | E.map_error | self.__handle_exception \
            | E.then | self.__repository.add_item \
            | E.map_error | self.__handle_exception

    def update_item(self, item: Dict[str, str]) -> E.Either[T, ServiceException]:
        return self.__validate_item(item) \
            | E.map_error | self.__handle_exception \
            | E.then | self.__repository.update_item \
            | E.map_error | self.__handle_exception

    def remove_item_by_id(self, id: str) -> E.Either[Dict[str, str], ServiceException]:
        return self.__repository.remove_item_by_id(id) \
            | E.map_error | self.__handle_exception \
            | E.then | (lambda removed_id: {"id": removed_id})