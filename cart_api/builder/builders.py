from flask import Flask, Blueprint, request
from flask.json import JSONEncoder
from signal import signal, SIGINT, SIGTERM
from typing import Callable, Dict
import python_either.either as E
from cart_api.core import Repository
from cart_api.domain import CartService
from cart_api.persistence import CartRepository, create_db_conn, DBConfiguration, Connection
from .helpers import handle_exception, handle_success
from datetime import date
import logging


class ApiJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


class ApiBuilder:
    def __init__(self, db_conn: Connection, service: Flask = Flask(__name__), should_listen_for_changes: bool = False):
        self.__db_conn = db_conn
        self.__service = service
        self.__should_listen_for_changes = should_listen_for_changes
    
    def add_resource(self, resource: Blueprint) -> 'ServiceBuilder':
        self.__service.register_blueprint(resource)
        return self

    def should_listen_for_changes(self) -> 'ServiceBuilder':
        self.__should_listen_for_changes = True
        return self

    def __listen_for_changes(self) -> None:
        def build_signal_receiver():
            def signal_received(signal_number, frame):
                try:
                    logging.info(f"Received signal '{signal_number}' - Closing database connection...")
                    self.__db_conn.close()
                    exit(0)
                except Exception as inst:
                    logging.error(inst.args)
                    exit(1)

            return signal_received 

        signal_receiver = build_signal_receiver()
        signal(SIGINT, signal_receiver)
        signal(SIGTERM, signal_receiver)

    def build(self) -> Flask:
        if self.__should_listen_for_changes:
            self.__listen_for_changes()
        
        self.__service.json_encoder = ApiJSONEncoder
        return self.__service


def build_healthcheck_endpoint(repository: Repository) -> Blueprint:
    endpoint = Blueprint('healthcheck', __name__)

    @endpoint.route('/healthcheck', methods=['GET'])
    def index():
        return repository.check_connection() | E.from_either | dict(
            if_success=(lambda _: handle_success("success")),
            if_failure=handle_exception
        )

    return endpoint


def build_cart_endpoint(repository: Repository) -> Blueprint:
    service = CartService(repository=repository)
    endpoint = Blueprint('cart', __name__, url_prefix="/cart")

    def __get_paginated_request(get_params: Callable[[str], str]) -> (int, int):
        page_number = get_params("page_number") or "0"
        page_size = get_params("page_size") or "10"
        return int(page_number), int(page_size)

    def __apply_id_to_body(body: Dict[str, str] = dict(), id: str = ""):
        body["id"] = id
        return body

    @endpoint.route('/', methods=['GET', 'POST'])
    def get_or_add_item():
        if request.method == 'POST':
            return service.add_item(request.get_json()) | E.from_either | dict(
                if_success=(lambda item: handle_success(item, 201)),
                if_failure=handle_exception
            )

        page_number, page_size = __get_paginated_request(request.args.get)
        return service.get_items(page_number, page_size) | E.from_either | dict(
            if_success=(lambda items: handle_success(items)),
            if_failure=handle_exception
        )

    @endpoint.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
    def get_or_update_item_by_id(id: int):
        if request.method == 'PUT':
            return E.success(__apply_id_to_body(request.get_json(), id)) \
                | E.then | service.update_item \
                | E.from_either | dict(
                    if_success=(lambda item: handle_success(item)),
                    if_failure=handle_exception
                )
        elif request.method == 'DELETE':
            return service.remove_item_by_id(id) | E.from_either | dict(
                    if_success=(lambda item: handle_success(item)),
                    if_failure=handle_exception
                )

        return service.get_item_by_id(id) | E.from_either | dict(
            if_success=(lambda item: handle_success(item)),
            if_failure=handle_exception
        )

    return endpoint


def build_cart_api(db_conn: Connection) -> Flask:
    repository = CartRepository(db_conn=db_conn)

    return ApiBuilder(db_conn=db_conn) \
        .add_resource(build_healthcheck_endpoint(repository)) \
        .add_resource(build_cart_endpoint(repository)) \
        .build()


def get_db_conn(get_config: Callable[[str], str]) -> E.Either[Connection, Exception]:
    logging.info("Attempting Database Connection...")
    return E.success(DBConfiguration(
        host=get_config("PYTHON_CART_DB_HOST"),
        username=get_config("PYTHON_CART_DB_USERNAME"),
        password=get_config("PYTHON_CART_DB_PASSWORD"),
        name=get_config("PYTHON_CART_DB_NAME"),
        port=int(get_config("PYTHON_CART_DB_PORT"))
    )) | E.then | create_db_conn
