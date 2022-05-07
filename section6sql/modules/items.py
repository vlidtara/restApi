import sqlite3
from db import db


class ItemModule:
    TABLE_NAME = "items"
    COL_1 = "name"
    COL_2 = "price"
    DB = "mydata.db"

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {self.COL_1: self.name, self.COL_2: self.price}

    @classmethod
    def find_by_user(cls, name):
        conn = sqlite3.connect(cls.DB)
        query = "SELECT * FROM {table} WHERE name=?".format(
            table=cls.TABLE_NAME)
        row = conn.cursor().execute(query, (name,)).fetchone()
        conn.close()
        if row:
            return cls(*row)

    @staticmethod
    def select_all():
        conn = sqlite3.connect(ItemModule.DB)
        query = "SELECT * FROM {table}".format(table=ItemModule.TABLE_NAME)
        row = conn.cursor().execute(query).fetchall()
        conn.close()
        return row

    @staticmethod
    def delete_by_user(name):
        conn = sqlite3.connect(ItemModule.DB)
        query = "DELETE FROM {table} WHERE name=?".format(
            table=ItemModule.TABLE_NAME)
        conn.cursor().execute(query, (name,))
        conn.commit()
        conn.close()

    def insert(self):
        conn = sqlite3.connect(self.DB)
        query = "INSERT INTO {table} VALUES(?,?)".format(table=self.TABLE_NAME)
        conn.cursor().execute(query, (self.name, self.price))
        conn.commit()
        conn.close()

    def update(self):
        conn = sqlite3.connect(self.DB)
        query = "UPDATE {table} SET {col2}=? WHERE {col1}=?".format(
            table=self.TABLE_NAME, col1=self.COL_1, col2=self.COL_2)
        conn.cursor().execute(query, (self.price, self.name))
        conn.commit()
        conn.close()
