from flask import Flask
from os import getenv
from typing import Callable
import python_either.either as E
from .builder import build_api_service
import logging

from dotenv import load_dotenv
from os import getenv


def create_api() -> Flask:
    load_dotenv()

    def __run_service(service: Flask) -> Flask:
        def __set_optional_config_variable(value: str, defaultValue: str = ""):
            service.config[value] = getenv(value) or defaultValue

        __set_optional_config_variable("ENV", "production")

        logging.info("Running server...")
        return service

    def __handle_exception(exception: Exception) -> None:
        logging.error(exception)
        exit(1)

    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    
    logging.info("Attempting Database Connection...")
    return build_api_service(getenv) | E.from_either | dict(
        if_success=__run_service,
        if_failure=__handle_exception
    )


def main():
    create_api().run(host='0.0.0.0')


if __name__ == "__main__":
    main()