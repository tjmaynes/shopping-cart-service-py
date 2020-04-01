from typing import Callable, List
import python_either.either as E
from pymysql import Connection
from cart_api.builder import get_db_conn
from cart_api.persistence import CartRepository
from cart_api.domain import CartService, CartItem
from os import getenv
from json import load as get_json_data
from cart_api.core import convert_list_to_either


def safely_load_json(filename: str) -> E.Either[CartItem, Exception]:
    with open(filename) as json_file:
        try:
            results = get_json_data(json_file)
            return E.success(results)
        except Exception as inst:
            return E.failure(inst)


def seed_cart_db(db_conn: Connection) -> E.Either[List[str], Exception]:
    def __seed_cart_db(raw_items: List[CartItem]) -> E.Either[List[E.Either[str, Exception]], Exception]:
        service = CartService(CartRepository(db_conn))
        return convert_list_to_either(list(map(service.add_item, raw_items)))

    return safely_load_json("cart_database/seed.json") | E.then | __seed_cart_db


def run() -> str:
    return get_db_conn(get_config=getenv) | E.then | seed_cart_db | E.from_either | dict(
        if_success=(lambda items: f"Seeded database with {len(items)} items!"),
        if_failure=(lambda ex: f"Unable to seed Cart database - {ex.args}!")
    )


if __name__ == "__main__":
    print(run())