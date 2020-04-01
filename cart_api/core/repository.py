from typing import List, TypeVar, Protocol
from .exceptions import RepositoryException
import python_either.either as E


T = TypeVar("T")


class Repository(Protocol[T]):

    def get_all_items(self, page_number: int, page_size: int) -> E.Either[List[T], RepositoryException]:
        pass

    def add_item(self, item: T) -> E.Either[T, RepositoryException]:
        pass

    def get_item_by_id(self, id: str) -> E.Either[T, RepositoryException]:
        pass

    def update_item(self, item: T) -> E.Either[T, RepositoryException]:
        pass

    def remove_item_by_id(self, id: str) -> E.Either[str, RepositoryException]:
        pass

    def create_database(self) -> E.Either[int, RepositoryException]:
        pass

    def check_connection(self) -> E.Either[str, RepositoryException]:
        pass