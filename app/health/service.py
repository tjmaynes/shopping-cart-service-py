from psycopg2 import Error as Psycopg2Error
from app.core import Connection
from .domain import Health

class HealthService:
    def __init__(self, db_conn: Connection):
        self.__db_conn = db_conn
        self.__db_cursor = db_conn.cursor()

    def check_health(self) -> Health:
        return Health(
            database_connected=self.__check_db_conn()
        )

    def __check_db_conn(self) -> bool:
        try:
            self.__db_cursor.execute("SELECT 1;")
            _ = self.__db_cursor.fetchone()
            self.__db_conn.commit()
            return True
        except Psycopg2Error as e:
            return False