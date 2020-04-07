from typing import List, TypeVar, Tuple
from cart_api.core import Repository, RepositoryException, UnknownException, NotFoundRepositoryException
from cart_api.domain import CartItem
from .db_conn import Connection
import python_either.either as E
import datetime


class CartRepository(Repository[CartItem]):

    def __init__(self, db_conn: Connection):
        self.__db_conn = db_conn


    def __from_tuple(self, tuple: Tuple) -> CartItem:
        return CartItem(
                id=tuple[0],
                name=tuple[1],
                price=tuple[2],
                manufacturer=tuple[3],
                updated_at=tuple[4],
                created_at=tuple[5]
            )


    def get_all_items(self, page_number: int = 0, page_size: int = 10) -> E.Either[List[CartItem], RepositoryException]:
        def get_limit(page_number: int, page_size: int) -> [int]:
            if page_number == 0:
                return [page_size, page_number]
            else:
                return [page_size, page_number * page_size]

        try:
            limit = get_limit(page_number=page_number, page_size=page_size)
            cursor = self.__db_conn.cursor()
            cursor.execute("SELECT id, name, price, manufacturer, updated_at, created_at FROM cart LIMIT %s OFFSET %s", limit)
            rows = cursor.fetchmany(size=page_size)
            if rows:
                return E.success(list(map(self.__from_tuple, rows)))
            return E.success([])

        except Exception as inst:
            return E.failure(UnknownException(list(inst.args)))


    def get_item_by_id(self, id: str) -> E.Either[CartItem, RepositoryException]:
        try:
            cursor = self.__db_conn.cursor()
            cursor.execute("SELECT id, name, price, manufacturer, updated_at, created_at FROM cart WHERE id = %s", [id])
            row = cursor.fetchone()
            if row:
                return E.success(self.__from_tuple(row))
            return E.failure(NotFoundRepositoryException())

        except Exception as inst:
            return E.failure(UnknownException(list(inst.args)))


    def add_item(self, item: CartItem) -> E.Either[CartItem, RepositoryException]:
        try:
            cursor = self.__db_conn.cursor()
            cursor.execute("INSERT INTO cart (name, price, manufacturer, updated_at, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING id, name, price, manufacturer, updated_at, created_at",
                [item.name, item.price, item.manufacturer, item.updated_at, item.created_at]
            )
            result = cursor.fetchone()
            self.__db_conn.commit()

            if result:
                return E.success(self.__from_tuple(result))
            return E.failure(UnknownException(["Unable to add item at this time!"]))

        except Exception as inst:
            self.__db_conn.rollback()
            return E.failure(UnknownException(list(inst.args)))


    def update_item(self, item: CartItem) -> E.Either[CartItem, RepositoryException]:
        try:
            cursor = self.__db_conn.cursor()
            cursor.execute("UPDATE cart SET name = %s, price = %s, manufacturer = %s, updated_at = %s WHERE id = %s RETURNING id, name, price, manufacturer, updated_at, created_at",
                [item.name, item.price, item.manufacturer, datetime.datetime.now().isoformat(), item.id]
            )
            result = cursor.fetchone()
            self.__db_conn.commit()
            if result:
                return E.success(self.__from_tuple(result))
            return E.failure(NotFoundRepositoryException())

        except Exception as inst:
            self.__db_conn.rollback()
            return E.failure(UnknownException(list(inst.args)))


    def remove_item_by_id(self, id: str) -> E.Either[str, RepositoryException]:
        try:
            cursor = self.__db_conn.cursor()
            cursor.execute("DELETE FROM cart WHERE id = %s", [id])
            rows_deleted = cursor.rowcount
            self.__db_conn.commit()

            if rows_deleted == 1:
                return E.success(id)
            return E.failure(NotFoundRepositoryException([id]))
        
        except Exception as inst:
            self.__db_conn.rollback()
            return E.failure(UnknownException(list(inst.args)))


    def create_database(self) -> E.Either[CartItem, RepositoryException]:
        try:
            cursor = self.__db_conn.cursor()
            results = cursor.execute("CREATE DATABASE IF NOT EXISTS cart")
            self.__db_conn.commit()
            return E.success(results)
        except Exception as inst:
            self.__db_conn.rollback()
            return E.failure(UnknownException(list(inst.args)))


    def check_connection(self) -> E.Either[str, RepositoryException]:
        try:
            cursor = self.__db_conn.cursor()
            cursor.execute("SELECT 1;")
            _ = cursor.fetchone()
            self.__db_conn.commit()
            return E.success("Success!")
        except Exception as inst:
            return E.failure(UnknownException(list(inst.args)))