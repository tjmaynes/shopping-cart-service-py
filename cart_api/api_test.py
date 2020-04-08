from flask import Flask, json
import python_either.either as E
from cart_api.builder import build_api_service
import cart_api.seed_database as seed_database
import cart_api.delete_database as delete_database
from typing import Dict

from unittest import TestCase, main
from unittest.mock import Mock, patch
from dotenv import load_dotenv
from os import getenv
import logging
import datetime


def build_client() -> Flask:
    def on_success(service: Flask):
        with service.test_client() as client:
            return client

    def on_failure(ex: Exception):
        logging.error(ex.args)
        exit(1)

    return build_api_service(getenv) | E.from_either | dict(
        if_success=on_success,
        if_failure=on_failure
    )

load_dotenv()
client = build_client()


class ApiTestSuite(TestCase):
    default_item = dict(name='hello', manufacturer='something', price=1900)

    def setUp(self):
        self.__client = client
        seed_database.run()


    def tearDown(self):
        delete_database.run()


    def test_healthcheck_endpoint_returns_200(self):
        response = self.__client.get('/healthcheck', content_type='application/json')

        assert 200 == response.status_code

        data = json.loads(response.data)
        assert data == "success"


    def test_cart_index_returns_10_items_from_cart(self):    
        response = self.__client.get('/cart/', content_type='application/json')
        assert 200 == response.status_code

        data = json.loads(response.data)
        assert len(data) == 10


    def test_cart_index_with_query_params_returns_list_of_available_cart_items(self):
        page_size = 20
        response = self.__client.get(f'/cart/?page_number=0&page_size={page_size}', content_type='application/json')

        assert 200 == response.status_code

        data = json.loads(response.data)
        assert len(data) == page_size


    def test_cart_get_item_by_id_returns_item(self):
        _, added_item = self.__add_item_to_db(self.default_item)

        status_code, data = self.__get_item_by_id_from_db(added_item["id"])

        assert 200 == status_code
        assert data["name"] == added_item["name"]
        assert data["price"] == added_item["price"]
        assert data["manufacturer"] == added_item["manufacturer"]
        assert data["updated_at"] == added_item["updated_at"]
        assert data["created_at"] == added_item["created_at"]


    def test_cart_add_item_returns_item(self):
        status_code, data = self.__add_item_to_db(self.default_item)

        assert 201 == status_code
        assert data["name"] == self.default_item["name"]
        assert data["price"] == self.default_item["price"]
        assert data["manufacturer"] == self.default_item["manufacturer"]

        self.__delete_item_from_db(data["id"])


    def test_cart_update_item_returns_item(self):
        _, added_item = self.__add_item_to_db(self.default_item)
        added_item["name"] = "a new name"

        datetime_mock = Mock(wraps=datetime.datetime)
        mocked_date_time = datetime.datetime(2000, 1, 1)
        datetime_mock.now.return_value = mocked_date_time

        with patch('datetime.datetime', new=datetime_mock):
            status_code, data = self.__update_item_in_db(added_item)

            assert 200 == status_code
            assert data["name"] == added_item["name"]
            assert data["price"] == added_item["price"]
            assert data["manufacturer"] == added_item["manufacturer"]
            assert data["created_at"] == added_item["created_at"]
            
            assert data["updated_at"] != added_item["updated_at"]
            assert data["updated_at"] == mocked_date_time.isoformat()


    def test_cart_delete_item_returns_id(self):
        _, item = self.__add_item_to_db(self.default_item)
        
        status_code, data = self.__delete_item_from_db(item["id"]) 
        
        assert 200 == status_code
        assert data["id"] == str(item["id"])


    def __parse_json_response(self, response):
        return response.status_code, json.loads(response.data)

    def __get_item_by_id_from_db(self, id: str):
        return self.__parse_json_response(self.__client.get(f'/cart/{id}', content_type='application/json'))

    def __add_item_to_db(self, item: Dict[str, str]):
        return self.__parse_json_response(self.__client.post('/cart/', data=json.dumps(item), content_type='application/json'))

    def __update_item_in_db(self, item: Dict[str, str]):
        return self.__parse_json_response(self.__client.put(f'/cart/{item["id"]}', data=json.dumps(item), content_type='application/json'))

    def __delete_item_from_db(self, id: str):
        return self.__parse_json_response(self.__client.delete(f'/cart/{id}', content_type='application/json'))


if __name__ == "__main__":
    main()