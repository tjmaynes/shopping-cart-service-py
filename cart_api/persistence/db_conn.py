from dataclasses import dataclass
import python_either.either as E
from cart_api.core import RepositoryException, ConnectionFailedRepositoryException
from psycopg2 import connect
from typing import Protocol, TypeVar
from urllib.parse import urlparse

T = TypeVar("T")


class Connection(Protocol[T]):
    def cursor(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        pass


@dataclass
class DBConfiguration:
    host: str
    username: str
    password: str
    name: str
    port: int


def parse_db_config(database_uri: str) -> DBConfiguration:
    result = urlparse(database_uri)
    return DBConfiguration(
        host=result.hostname,
        username=result.username,
        password=result.password,
        name=result.path[1:],
        port=result.port
    )


# TODO: def retry(e: Either[Any, Any], retry_duration: int = 3, retry_count: int = 3) -> Either[Any, Any]:
def create_db_conn(database_uri: str) -> E.Either[Connection, RepositoryException]:
    try:
        config = parse_db_config(database_uri)
        return E.success(connect(host=config.host, user=config.username, password=config.password, dbname=config.name, port=config.port))
    except Exception as inst:
        return E.failure(ConnectionFailedRepositoryException(list(inst.args)))
