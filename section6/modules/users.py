import sqlite3

class UserModule:
    TABLE_NAME = "users"

    def __init__(self,_id,username,password) -> None:
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('mydata.db')
        cursor = connection.cursor()
        query = "SELECT * FROM {table} WHERE username=?".format(table=cls.TABLE_NAME)
        print(username)
        row = cursor.execute(query,(username,)).fetchone()
        return cls(*row) if row else None
    
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('mydata.db')
        cursor = connection.cursor()
        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        row = cursor.execute(query,(_id,)).fetchone()
        return cls(*row) if row else None
