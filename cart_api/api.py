from flask import Flask
from os import getenv
from typing import Callable
import logging
import python_either.either as E
from .builder import get_db_conn, build_cart_api


def build_api_service(get_config: Callable[[str], str]) -> E.Either[Flask, Exception]:
    return get_db_conn(get_config) | E.then | build_cart_api


def create_api() -> Flask:
    def run_service(service: Flask) -> Flask:
        logging.info("Running server...")
        return service

    def handle_exception(exception: Exception) -> None:
        logging.error(exception)
        exit(1)

    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    
    return build_api_service(getenv) | E.from_either | dict(
        if_success=run_service,
        if_failure=handle_exception
    )


def main():
    create_api().run(port=3000)


if __name__ == "__main__":
    main()