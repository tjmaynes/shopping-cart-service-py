from shoppingcart.utils import get_env_var_or_throw
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from psycopg import connect
from result import Ok
from typing import List, Dict
from shoppingcart.core import InvalidItemException, NotFoundException
from shoppingcart.cart import CartService, CartRepository, CartItem, CartItemIn
from shoppingcart.health import HealthService


def build_api() -> FastAPI:
    db_conn = connect(get_env_var_or_throw("DATABASE_URL"))

    health_service = HealthService(db_conn=db_conn)
    cart_repository = CartRepository(db_conn=db_conn)
    cart_service = CartService(repository=cart_repository)

    app = FastAPI()

    @app.get("/health")
    async def health_endpoint():
        health = health_service.check_health()
        if health.database_connected:
            return JSONResponse(status_code=200, content=jsonable_encoder(health))
        else:
            return JSONResponse(status_code=500, detail=jsonable_encoder(health))

    @app.get("/cart", response_model=List[CartItem])
    async def fetch_cart_items(page_number: int = 0, page_size: int = 10):
        items_result = cart_service.get_items(page_number, page_size)
        if isinstance(items_result, Ok):
            return JSONResponse(
                status_code=200, content=jsonable_encoder(items_result.ok_value)
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=jsonable_encoder({"error": items_result.err_value.message}),
            )

    @app.get("/cart/{id}", response_model=CartItem)
    async def fetch_item_by_id(id: str):
        item_result = cart_service.get_item_by_id(id)
        if isinstance(item_result, Ok):
            return JSONResponse(
                status_code=200, content=jsonable_encoder(item_result.ok_value)
            )
        elif isinstance(item_result.err_value, NotFoundException):
            raise HTTPException(status_code=404)
        else:
            raise HTTPException(
                status_code=500,
                detail=jsonable_encoder({"error": item_result.err_value.message}),
            )

    @app.post("/cart/", response_model=CartItem)
    async def create_cart_item(item: CartItemIn):
        add_item_result = cart_service.add_item(item)
        if isinstance(add_item_result, Ok):
            return JSONResponse(
                status_code=201, content=jsonable_encoder(add_item_result.ok_value)
            )
        elif isinstance(add_item_result.err_value, InvalidItemException):
            raise HTTPException(
                status_code=422,
                detail=jsonable_encoder({"error": add_item_result.err_value.message}),
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=jsonable_encoder({"error": add_item_result.err_value.message}),
            )

    @app.put("/cart/{id}", response_model=CartItem)
    async def update_cart_item(id: str, item: CartItemIn):
        update_item_result = cart_service.update_item(id, item)
        if isinstance(update_item_result, Ok):
            return jsonable_encoder(update_item_result.ok_value)
        elif isinstance(update_item_result.err_value, InvalidItemException):
            raise HTTPException(
                status_code=422,
                detail=jsonable_encoder(
                    {"error": update_item_result.err_value.message}
                ),
            )
        elif isinstance(update_item_result.err_value, NotFoundException):
            raise HTTPException(status_code=404)
        else:
            raise HTTPException(
                status_code=500,
                detail=jsonable_encoder(
                    {"error": update_item_result.err_value.message}
                ),
            )

    @app.delete("/cart/{id}", response_model=Dict)
    async def delete_cart_item(id: str):
        delete_item_result = cart_service.remove_item_by_id(id)
        if isinstance(delete_item_result, Ok):
            return jsonable_encoder({"id": delete_item_result.ok_value})
        elif isinstance(delete_item_result.err_value, NotFoundException):
            raise HTTPException(status_code=404)
        else:
            raise HTTPException(
                status_code=500,
                detail=jsonable_encoder(
                    {"error": delete_item_result.err_value.message}
                ),
            )

    return app


api = build_api()
