from typing import List, TypeVar
from pymysql import connect, Connection
from cart_api.core import Repository, RepositoryException, UnknownException, NotFoundRepositoryException
from cart_api.domain import CartItem
import python_either.either as E


class CartRepository(Repository[CartItem]):

    def __init__(self, db_conn: Connection):
        self.__db_conn = db_conn


    def get_all_items(self, page_number: int = 0, page_size: int = 10) -> E.Either[List[CartItem], RepositoryException]:
        def get_limit(page_number: int, page_size: int) -> (int, int):
            if page_number == 0:
                return page_number, page_size
            else:
                return page_number * page_size, (page_number * page_size) + page_size

        try:
            current_row, to_row = get_limit(page_number=page_number, page_size=page_size)
            cursor = self.__db_conn.cursor()
            cursor.execute("SELECT id, name, price, manufacturer FROM cart LIMIT %s, %s", (current_row, to_row))
            rows = cursor.fetchmany(size=page_size)
            if rows:
                return E.success(rows)
            return E.success([])

        except Exception as inst:
            return E.failure(UnknownException(list(inst.args)))


    def get_item_by_id(self, id: str) -> E.Either[CartItem, RepositoryException]:
        try:
            cursor = self.__db_conn.cursor()
            cursor.execute("SELECT id, name, price, manufacturer FROM cart WHERE id = %s", (id))
            row = cursor.fetchone()
            if row:
                return E.success(row)
            return E.failure(NotFoundRepositoryException())

        except Exception as inst:
            return E.failure(UnknownException(list(inst.args)))


    def add_item(self, item: CartItem) -> E.Either[CartItem, RepositoryException]:
        try:
            cursor = self.__db_conn.cursor()
            _ = cursor.execute("INSERT INTO `cart` (`name`, `price`, `manufacturer`) VALUES (%s, %s, %s);",
                (item.name, item.price, item.manufacturer)
            )
            new_id = cursor.lastrowid
            self.__db_conn.commit()

            cursor.execute("SELECT id, name, price, manufacturer FROM cart WHERE id = %s", (new_id))
            result = cursor.fetchone()
            if result:
                return E.success(result)
            return E.failure(UnknownException(["Unable to add item at this time!"]))

        except Exception as inst:
            return E.failure(UnknownException(list(inst.args)))


    def update_item(self, item: CartItem) -> E.Either[CartItem, RepositoryException]:
        try:
            cursor = self.__db_conn.cursor()
            _ = cursor.execute("UPDATE cart SET `name` = %s, `price` = %s, `manufacturer` = %s WHERE id = %s;",
                (item.name, item.price, item.manufacturer, item.id)
            )
            self.__db_conn.commit()

            cursor.execute("SELECT id, name, price, manufacturer FROM cart WHERE id = %s", (item.id))
            result = cursor.fetchone()
            if result:
                return E.success(result)
            return E.failure(NotFoundRepositoryException())

        except Exception as inst:
            return E.failure(UnknownException(list(inst.args)))


    def remove_item_by_id(self, id: str) -> E.Either[str, RepositoryException]:
        try:
            cursor = self.__db_conn.cursor()
            result = cursor.execute("DELETE FROM cart WHERE id = %s;", (id))
            self.__db_conn.commit()

            if result == "0":
                return E.failure(NotFoundRepositoryException([id]))
            return E.success(id)
        
        except Exception as inst:
            return E.failure(UnknownException(list(inst.args)))


    def create_database(self) -> E.Either[CartItem, RepositoryException]:
        try:
            cursor = self.__db_conn.cursor()
            results = cursor.execute("CREATE DATABASE IF NOT EXISTS cart")
            self.__db_conn.commit()
            return E.success(results)
        except Exception as inst:
            return E.failure(UnknownException(list(inst.args)))


    def check_connection(self) -> E.Either[str, RepositoryException]:
        try:
            cursor = self.__db_conn.cursor()
            cursor.execute("SELECT VERSION()")
            _ = cursor.fetchone()
            return E.success("Success!")
        except Exception as inst:
            return E.failure(UnknownException(list(inst.args)))