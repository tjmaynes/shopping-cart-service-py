from typing import Callable, Dict, Any, List
from psycopg2 import connect
from result import Ok, Err, Result
from os import getenv
from json import load as get_json_data
from app.cart import CartService, CartRepository, CartItemIn


def safely_load_json(filename: str) -> Result[List[Dict[str, Any]], Exception]:
    with open(filename) as json_file:
        try:
            return Ok(get_json_data(json_file))
        except Exception as inst:
            return Err(inst)


def seed_db() -> str:
    seed_result = safely_load_json("db/seed.json")

    if isinstance(seed_result, Ok):
        db_conn = connect(getenv("DATABASE_URL"))
        service = CartService(CartRepository(db_conn))

        for item in seed_result.ok_value:
            service.add_item(CartItemIn(
                name = item["name"],
                manufacturer = item["manufacturer"],
                price = item["price"]
            ))

        return f"Seeded database with {len(seed_result.ok_value)} items!"
    else:
        return f"Unable to seed database: {seed_result.err_value}"


if __name__ == "__main__":
    print(seed_db())