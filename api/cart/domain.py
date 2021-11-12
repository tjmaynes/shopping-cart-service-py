from typing import List, Dict, Callable, Any, Tuple
from dataclasses import dataclass, field
from result import Ok, Err, Result
from pydantic import BaseModel
from datetime import datetime
from api.core import InvalidItemException, CustomException

class CartItemIn(BaseModel):
    name: str
    price: int
    manufacturer: str

class CartItem(BaseModel):
    id: str
    name: str
    price: int
    manufacturer: str
    created_at: datetime
    last_modified_at: datetime

def validate_cart_item(item: CartItemIn) -> Result[CartItemIn, CustomException]:
    def empty_value(type: str) -> str:
        return f"'{type}' must not be empty"

    errors: List[str] = []

    if item.name is None:
        errors.append(empty_value("name"))
    elif len(item.name) == 0:
        errors.append(empty_value("name"))
    
    if item.price is None:
        errors.append(empty_value("price"))
    if int(item.price) < 99:
        errors.append("'price' must be greater than 99")

    if item.manufacturer is None:
        errors.append(empty_value("manufacturer"))
    if len(item.manufacturer) == 0:
        errors.append(empty_value("manufacturer"))

    if len(errors) != 0:
        return Err(InvalidItemException(errors))
    else:
        return Ok(item)