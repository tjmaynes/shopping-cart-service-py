from typing import List, TypeVar, Protocol
from result import Ok, Err, Result
from .exceptions import CustomException

S = TypeVar("S", contravariant=True)
T = TypeVar("T")


class Repository(Protocol[S, T]):

    def get_all_items(self, page_number: int, page_size: int) -> Result[List[T], CustomException]:
        pass

    def add_item(self, item: S) -> Result[T, CustomException]:
        pass

    def get_item_by_id(self, id: str) -> Result[T, CustomException]:
        pass

    def update_item(self, id: str, item: S) -> Result[T, CustomException]:
        pass

    def remove_item_by_id(self, id: str) -> Result[str, CustomException]:
        pass