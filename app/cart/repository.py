from typing import List, TypeVar, Tuple
from app.core import Repository, CustomException, UnknownException, NotFoundException, Connection
from .domain import CartItem, CartItemIn
from result import Ok, Err, Result
import datetime

class CartRepository(Repository[CartItemIn, CartItem]):

    def __init__(self, db_conn: Connection):
        self.__db_conn = db_conn

    def get_all_items(self, page_number: int = 0, page_size: int = 10) -> Result[List[CartItem], CustomException]:
        try:
            cursor = self.__db_conn.cursor()
            cursor.execute("SELECT id, name, price, manufacturer, last_modified_at, created_at FROM cart LIMIT %s OFFSET %s", [page_size, page_number * page_size])
            rows = cursor.fetchmany(size=page_size)
            if rows:
                return Ok(list(map(self.__from_tuple, rows)))
            return Ok([])

        except Exception as inst:
            return Err(UnknownException(inst))


    def get_item_by_id(self, id: str) -> Result[CartItem, CustomException]:
        try:
            cursor = self.__db_conn.cursor()
            cursor.execute("SELECT id, name, price, manufacturer, last_modified_at, created_at FROM cart WHERE id = %s", [id])
            row = cursor.fetchone()
            if row:
                return Ok(self.__from_tuple(row))
            return Err(NotFoundException(message="id: {}".format(id)))

        except Exception as inst:
            return Err(UnknownException(inst))


    def add_item(self, item: CartItemIn) -> Result[CartItem, CustomException]:
        try:
            cursor = self.__db_conn.cursor()
            cursor.execute("INSERT INTO cart (name, price, manufacturer) VALUES (%s, %s, %s) RETURNING id, name, price, manufacturer, last_modified_at, created_at",
                [item.name, item.price, item.manufacturer]
            )
            result = cursor.fetchone()
            self.__db_conn.commit()

            if result:
                return Ok(self.__from_tuple(result))
            return Err(UnknownException("Unable to add item at this time!"))

        except Exception as inst:
            self.__db_conn.rollback()
            return Err(UnknownException(inst))


    def update_item(self, id: str, item: CartItemIn) -> Result[CartItem, CustomException]:
        try:
            cursor = self.__db_conn.cursor()
            cursor.execute("UPDATE cart SET name = %s, price = %s, manufacturer = %s WHERE id = %s RETURNING id, name, price, manufacturer, last_modified_at, created_at",
                [item.name, item.price, item.manufacturer, id]
            )
            result = cursor.fetchone()
            self.__db_conn.commit()
            if result:
                return Ok(self.__from_tuple(result))
            return Err(NotFoundException(message="id: {}".format(id)))

        except Exception as inst:
            self.__db_conn.rollback()
            return Err(UnknownException(inst))


    def remove_item_by_id(self, id: str) -> Result[str, CustomException]:
        try:
            cursor = self.__db_conn.cursor()
            cursor.execute("DELETE FROM cart WHERE id = %s", [id])
            rows_deleted = cursor.rowcount
            self.__db_conn.commit()

            if rows_deleted == 1:
                return Ok(id)
            return Err(NotFoundException(message="id: {}".format(id)))
        
        except Exception as inst:
            self.__db_conn.rollback()
            return Err(UnknownException(inst))


    def __from_tuple(self, tuple: Tuple) -> CartItem:
        return CartItem(
                id="{}".format(tuple[0]),
                name=tuple[1],
                price=tuple[2],
                manufacturer=tuple[3],
                last_modified_at=tuple[4],
                created_at=tuple[5]
            )


