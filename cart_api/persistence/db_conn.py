from pymysql import connect, Connection, cursors
from dataclasses import dataclass
import python_either.either as E
from cart_api.core import RepositoryException, ConnectionFailedRepositoryException


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
        return E.success(connect(host=config.host, user=config.username, passwd=config.password, db=config.name, port=config.port,cursorclass=cursors.DictCursor))
    except Exception as inst:
        return E.failure(ConnectionFailedRepositoryException(list(inst.args)))
