from dataclasses import dataclass
import python_either.either as E
from cart_api.core import RepositoryException, ConnectionFailedRepositoryException
from psycopg2 import connect
from typing import Protocol, TypeVar


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


# TODO: def retry(e: Either[Any, Any], retry_duration: int = 3, retry_count: int = 3) -> Either[Any, Any]:

def create_db_conn(config: DBConfiguration) -> E.Either[Connection, RepositoryException]:
    try:
        return E.success(connect(host=config.host, user=config.username, password=config.password, dbname=config.name, port=config.port))
    except Exception as inst:
        return E.failure(ConnectionFailedRepositoryException(list(inst.args)))
