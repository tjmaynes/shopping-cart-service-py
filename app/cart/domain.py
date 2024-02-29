from typing import List, Dict, Callable, Any, Tuple
from dataclasses import dataclass, field
from result import Ok, Err, Result
from pydantic import BaseModel
from datetime import datetime
from app.core import InvalidItemException, CustomException

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
    errors = []

    if not item.name or len(item.name) == 0:
        errors.append("'name' must not be empty")

    if item.price is None or int(item.price) < 99:
        errors.append("'price' must be a non-empty number greater than 99")

    if not item.manufacturer or len(item.manufacturer) == 0:
        errors.append("'manufacturer' must not be empty")

    if errors:
        return Err(InvalidItemException(errors))
    else:
        return Ok(item)