from typing import List
import python_either.either as E
from pymysql import Connection
from cart_api.core import convert_list_to_either
from cart_api.builder import get_db_conn
from cart_api.persistence import CartRepository
from cart_api.domain import CartService, CartItem
from os import getenv
from json import load as get_json_data


def safely_load_json(filename: str) -> E.Either[CartItem, Exception]:
    with open(filename) as json_file:
        try:
            results = get_json_data(json_file)
            return E.success(results)
        except Exception as inst:
            return E.failure(inst)


def delete_cart_db(db_conn: Connection) -> E.Either[List[str], Exception]:
    def __delete_cart_db(raw_items: List[CartItem]) -> E.Either[List[str], Exception]:
        service = CartService(CartRepository(db_conn))
        results = []
        for index in range(len(raw_items)):
            results.append(service.remove_item_by_id(index))
        return convert_list_to_either(results)

    return safely_load_json("cart_database/seed.json") | E.then | __delete_cart_db


def run() -> str:
    return get_db_conn(get_config=getenv) | E.then | delete_cart_db | E.from_either | dict(
        if_success=(lambda results: f"Deleting {len(results)} items from database!"),
        if_failure=(lambda ex: f"Unable to delete Cart database - {ex}!")
    )


if __name__ == "__main__":
    print(run())