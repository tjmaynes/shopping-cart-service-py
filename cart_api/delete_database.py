from typing import List
import python_either.either as E
from cart_api.core import convert_list_to_either
from cart_api.builder import get_db_conn
from cart_api.persistence import CartRepository, Connection
from cart_api.domain import CartService, CartItem
from os import getenv


def delete_cart_db(db_conn: Connection) -> E.Either[List[str], Exception]:
    service = CartService(CartRepository(db_conn))

    def __get_all_cart_items_in_db(current_page: int = 0, page_size: int = 20, items: List[CartItem] = []) -> E.Either[List[CartItem], Exception]:
        def __check_result(items: List[CartItem] = []) -> E.Either[List[CartItem], Exception]:
            if len(items) <= 0:
                return E.failure("No more items!")
            else:
                return E.success(items)
        
        return service.get_items(page_number=current_page, page_size=page_size) \
            | E.then | __check_result \
            | E.from_either | dict(
                if_success=(lambda results: __get_all_cart_items_in_db(current_page=current_page + 1, page_size=page_size, items= items + results)),
                if_failure=(lambda ex: E.success(items))
            )

    def __delete_cart_db(items: List[CartItem]) -> E.Either[List[str], Exception]:
        results = []
        for item in items:
            results.append(service.remove_item_by_id(item.id))
        return convert_list_to_either(results)

    return __get_all_cart_items_in_db() | E.then | __delete_cart_db


def run() -> str:
    return get_db_conn(get_config=getenv) | E.then | delete_cart_db | E.from_either | dict(
        if_success=(lambda results: f"Deleting {len(results)} items from database!"),
        if_failure=(lambda ex: f"Unable to delete Cart database - {ex}!")
    )


if __name__ == "__main__":
    print(run())