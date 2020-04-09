from typing import Callable, List
import python_either.either as E
from cart_api.core import Service, Repository
from .cart_item import CartItem

def CartService(repository: Repository) -> Service[CartItem]:
    return Service(repository, CartItem.validate)
