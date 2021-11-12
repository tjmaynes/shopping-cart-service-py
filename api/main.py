from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from psycopg2 import connect
from result import Ok, Err, Result
from typing import List, Dict
import json
from os import getenv
from api.core import CustomException, InvalidItemException, NotFoundException
from api.cart import CartService, CartRepository, CartItem, CartItemIn
from api.health import HealthService, Health    

def build_app() -> FastAPI:
    db_conn = connect(getenv("DATABASE_URL"))
    
    health_service = HealthService(db_conn = db_conn)
    cart_repository = CartRepository(db_conn = db_conn)
    cart_service = CartService(repository = cart_repository)

    app = FastAPI()

    @app.get("/health")
    async def health_endpoint() -> JSONResponse:
        health = health_service.check_health()
        if health.database_connected:
            return JSONResponse(status_code=200, content=jsonable_encoder(health))
        else:
            return JSONResponse(status_code=500, content=jsonable_encoder(health))

    @app.get("/cart/", response_model=List[CartItem])
    async def fetch_cart_items(page_number: int = 0, page_size: int = 10) -> JSONResponse:
        items_result = cart_service.get_items(page_number, page_size)
        if isinstance(items_result, Ok):
            return JSONResponse(status_code=200, content=jsonable_encoder(items_result.value))
        else:
            return JSONResponse(status_code=500, content=jsonable_encoder(items_result.value))

    @app.get("/cart/{id}", response_model=CartItem)
    async def fetch_item_by_id(id: str) -> JSONResponse:
        item_result = cart_service.get_item_by_id(id)
        if isinstance(item_result, Ok):
            return JSONResponse(status_code=200, content=jsonable_encoder(item_result.value))
        else:
            return JSONResponse(status_code=500, content=jsonable_encoder(item_result.value))

    @app.post("/cart/", response_model=CartItem)
    async def create_cart_item(item: CartItemIn) -> JSONResponse:
        add_item_result = cart_service.add_item(item)
        if isinstance(add_item_result, Ok):
            return JSONResponse(status_code=201, content=jsonable_encoder(add_item_result.value))
        else:
            if isinstance(add_item_result.value, InvalidItemException):
                return JSONResponse(status_code=422, content=str(add_item_result.value))
            else:
                return JSONResponse(status_code=500, content=jsonable_encoder(add_item_result.value))

    @app.put("/cart/{id}", response_model=CartItem)
    async def update_cart_item(id: str, item: CartItem) -> JSONResponse:
        update_item_result = cart_service.update_item(id, item)
        if isinstance(update_item_result, Ok):
            return JSONResponse(status_code=200, content=jsonable_encoder(update_item_result.value))
        else:
            if isinstance(update_item_result.value, InvalidItemException):
                return JSONResponse(status_code=422, content=str(update_item_result.value))
            else:
                return JSONResponse(status_code=500, content=jsonable_encoder(update_item_result.value))

    @app.delete("/cart/{id}", response_model=Dict)
    async def update_cart_item(id: str) -> JSONResponse:
        update_item_result = cart_service.remove_item_by_id(id)
        if isinstance(update_item_result, Ok):
            return JSONResponse(status_code=200, content=jsonable_encoder({ "id": update_item_result.value }))
        else:
            if isinstance(update_item_result.value, NotFoundException):
                return JSONResponse(status_code=404, content=str(update_item_result.value))
            else:
                return JSONResponse(status_code=500, content=jsonable_encoder(update_item_result.value))

    return app

app = build_app()