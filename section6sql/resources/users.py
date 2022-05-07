import sqlite3
from  modules.users import UserModule
from flask_restful import Resource, reqparse


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
        if UserModule.find_by_username(data['username']):
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
