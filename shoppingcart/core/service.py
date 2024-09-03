from typing import List, Callable, TypeVar, Generic
from result import Ok, Result
from .repository import Repository
from .exceptions import CustomException

S = TypeVar("S")
T = TypeVar("T")


class Service(Generic[S, T]):
    def __init__(
        self,
        repository: Repository,
        validate_item: Callable[[S], Result[S, CustomException]],
    ):
        self.__repository = repository
        self.__validate_item = validate_item

    def get_items(
        self, page_number: int = 0, page_size: int = 10
    ) -> Result[List[T], CustomException]:
        return self.__repository.get_all_items(page_number, page_size)

    def get_item_by_id(self, id: str) -> Result[T, CustomException]:
        return self.__repository.get_item_by_id(id)

    def add_item(self, item: S) -> Result[T, CustomException]:
        validation_result = self.__validate_item(item)
        if isinstance(validation_result, Ok):
            return self.__repository.add_item(validation_result.ok_value)
        else:
            return validation_result

    def update_item(self, id: str, item: S) -> Result[T, CustomException]:
        validation_result = self.__validate_item(item)
        if isinstance(validation_result, Ok):
            return self.__repository.update_item(id, validation_result.ok_value)
        else:
            return validation_result

    def remove_item_by_id(self, id: str) -> Result[str, CustomException]:
        return self.__repository.remove_item_by_id(id)
