from typing import Callable, List
from app.core import Service, Repository
from .domain import CartItem, CartItemIn, validate_cart_item

def CartService(repository: Repository) -> Service[CartItemIn, CartItem]:
    return Service(repository, validate_cart_item)