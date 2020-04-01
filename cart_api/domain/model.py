from typing import List, Dict, Callable
from dataclasses import dataclass, field
import python_either.either as E
from cart_api.core import InvalidItemException

def validate_string(obj: Dict[str, str], key: str = "") -> E.Either[str, List[str]]:
    def empty_value(type: str) -> str: f"'{type}' must not be empty"

    errors: List[str] = []
    if obj[key] is None:
        errors.append(empty_value(key))
    elif len(obj[key]) == 0:
        errors.append(empty_value(key))
    
    return obj[key] if len(errors) == 0 else errors


def validate_int(obj: Dict[str, str], greater_than: Callable[[int], bool], key: str = "") -> E.Either[int, List[int]]:
    def empty_value(type: str) -> str: f"'{type}' must not be empty"

    errors: List[str] = []
    if obj[key] is None:
        errors.append(empty_value(key))
    elif greater_than(int(obj[key])):
        errors.append(f"'{key}' must be greater than '{int(obj[key])}'")
    
    return int(obj[key]) if len(errors) == 0 else errors


@dataclass
class CartItem:
    name: str
    price: int
    manufacturer: str
    id: str


    @staticmethod
    def validate(item: Dict[str, str]) -> E.Either['CartItem', Exception]:
        def empty_value(type: str) -> str:
            return f"'{type}' must not be empty"
        
        def get_optional_value(key: str) -> str:
            if key in item:
                return item[key]
            else:
                return ""

        errors: List[str] = []

        if item["name"] is None:
            errors.append(empty_value("name"))
        elif len(item["name"]) == 0:
            errors.append(empty_value("name"))
        
        if item["price"] is None:
            errors.append(empty_value("price"))
        if int(item["price"]) < 99:
            errors.append("'price' must be greater than 99")

        if item["manufacturer"] is None:
            errors.append(empty_value("manufacturer"))
        if len(item["manufacturer"]) == 0:
            errors.append(empty_value("manufacturer"))

        if len(errors) != 0:
            return E.failure(InvalidItemException(errors))
        else:
            return E.success(CartItem(
                id=get_optional_value("id"),
                name=item["name"],
                price=item["price"],
                manufacturer=item["manufacturer"]
            ))