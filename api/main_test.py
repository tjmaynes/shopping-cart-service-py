import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.core import Connection
from api.main import app
from api.seed import seed_db
from typing import Dict, Any
from psycopg2 import connect
from os import getenv
from datetime import datetime


class TestApi:
    @pytest.fixture
    def client(self):
        yield TestClient(app)

    @pytest.fixture
    def default_cart_item(self) -> Dict:
        yield dict(name='hello', manufacturer='something', price=1800)

    @pytest.fixture
    def db_conn(self):
        yield connect(getenv("DATABASE_URL"))

    def test_health_endpoint_returns_200_when_db_conn_is_connected(self, client: TestClient):
        response = client.get('/health')

        assert response.status_code == 200
        assert response.json() == {"database_connected": True}

    def test_cart_index_returns_items_from_cart(self, client: TestClient, db_conn: Connection):
        seed_db()

        response = client.get('/cart/')
        assert 200 == response.status_code

        assert len(response.json()) == 10

        page_size = 20
        response = client.get(f'/cart/?page_number=0&page_size={page_size}')

        assert 200 == response.status_code
        assert len(response.json()) == page_size

        self.__delete_db(db_conn)


    def test_cart_get_item_by_id_returns_item(self, client: TestClient, default_cart_item: Dict):
        _, added_item = self.__add_item(client, default_cart_item)

        status_code, data = self.__get_item_by_id(client, added_item["id"])

        assert 200 == status_code
        assert data["name"] == added_item["name"]
        assert data["price"] == added_item["price"]
        assert data["manufacturer"] == added_item["manufacturer"]
        assert data["last_modified_at"] == added_item["last_modified_at"]
        assert data["created_at"] == added_item["created_at"]


    def test_cart_add_item_returns_item(self, client, default_cart_item):
        status_code, data = self.__add_item(client, default_cart_item)

        assert 201 == status_code
        assert data["name"] == default_cart_item["name"]
        assert data["price"] == default_cart_item["price"]
        assert data["manufacturer"] == default_cart_item["manufacturer"]

    def test_cart_update_item_returns_item(self, client: TestClient, default_cart_item: Dict):
        _, added_item = self.__add_item(client, default_cart_item)
        added_item["name"] = "a new name"

        status_code, data = self.__update_item(client, added_item)

        assert 200 == status_code
        assert data["name"] == added_item["name"]
        assert data["price"] == added_item["price"]
        assert data["manufacturer"] == added_item["manufacturer"]
        assert data["created_at"] == added_item["created_at"]
    
        self.__delete_item(client, data["id"])


    def test_cart_delete_item_returns_id(self, client: TestClient, default_cart_item: Dict):
        _, item = self.__add_item(client, default_cart_item)
        
        status_code, data = self.__delete_item(client, item["id"])

        print(f"what = {data}")

        assert 200 == status_code
        assert data["id"] == str(item["id"])


    def __parse_json_response(self, response):
        return response.status_code, response.json()

    def __get_item_by_id(self, client: TestClient, id: str):
        return self.__parse_json_response(client.get(f'/cart/{id}'))

    def __add_item(self, client: TestClient, item: Dict[str, Any]):
        return self.__parse_json_response(client.post('/cart/', json=item))

    def __update_item(self, client: TestClient, item: Dict[str, Any]):
        return self.__parse_json_response(client.put(f'/cart/{item["id"]}', json=item))

    def __delete_item(self, client: TestClient, id: str):
        return self.__parse_json_response(client.delete(f'/cart/{id}'))

    def __delete_db(self, db_conn: Connection):
        try:
            cursor = db_conn.cursor()
            cursor.execute("DELETE FROM cart")
            db_conn.commit()
        except Exception as inst:
            print(f"Failed to delete db: {list(inst.args)}")
            db_conn.rollback()
