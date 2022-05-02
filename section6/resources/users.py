import sqlite3
from flask_restful import Resource, reqparse

class Users:
    def __init__(self,_id,username,password) -> None:
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('mydata.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        print(username)
        row = cursor.execute(query,(username,)).fetchone()
        return cls(*row) if row else None
    
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        row = cursor.execute(query,(_id,)).fetchone()
        return cls(*row) if row else None


class Register(Resource):
    TABLE_NAME = "users"

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = Register.parser.parse_args()
        if Users.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400
        conn = sqlite3.connect('mydata.db')
        cursor = conn.cursor()
        query = '''
            INSERT INTO {table} VALUES (NULL, ?, ?)
        '''.format(table=self.TABLE_NAME)
        cursor.execute(query,(data['username'],data['password']))
        conn.commit()
        conn.close()
        return {"message": "User created successfully."}, 201
