import re
from xmlrpc.client import Boolean
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from typing import *

items = []

class Item(Resource):
    TABLE_NAME = "items"

    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float,required=True,help="This field cannot be left blank!")

    @classmethod
    def find_by_user(cls,name):
        conn = sqlite3.connect('mydata.db')
        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        row = conn.cursor().execute(query,(name,)).fetchone()
        conn.close()
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
         
    @classmethod
    def insert(cls, item):
        conn = sqlite3.connect('mydata.db')
        query = "INSERT INTO {table} VALUES(?,?)".format(table=cls.TABLE_NAME)
        conn.cursor().execute(query,(item["name"], item["price"]))
        conn.commit()
        conn.close()
    
    @classmethod
    def update(cls, item):
        conn = sqlite3.connect('mydata.db')
        query = "UPDATE {table} SET {col1}=? WHERE {col0}=?".format(table=cls.TABLE_NAME,col0="name",col1="price")
        conn.cursor().execute(query,(item["price"],item["name"]))
        conn.commit()
        conn.close()

        
    #@jwt_required()
    def get(self, name):
        item = self.find_by_user(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404
        
        
    #@jwt_required()
    def post(self, name):
        if self.find_by_user(name):
            return {'message': "An item with name '{}' already exists.".format(name)}
        else:
            new_item = {
                "name": name,
                "price": Item.parser.parse_args()["price"]
            }
            try:
                self.insert(new_item)
            except:
                return {"message": "An error occurred inserting the item."}, 500
            return new_item, 201
            
    def put(self, name):
        new_item = {
            "name": name,
            "price": Item.parser.parse_args()["price"]
        }       
        if self.find_by_user(name):
            try:
                self.update(new_item)
            except:
                return {"message": "An error occurred updating the item."}, 500
            return {'message': "An item with name '{}' is updated.".format(name)}
        else:
            try:
                self.insert(new_item)
            except:
                return {"message": "An error occurred inserting the item."}, 500
            return {'message': "An item with name '{}' is created.".format(name)}

   
    #@jwt_required()
    def delete(self, name):
        if self.find_by_user(name):
            conn = sqlite3.connect('mydata.db')
            query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
            conn.cursor().execute(query,(name,))
            conn.commit()
            conn.close()
            return {'message': "An item with name '{}' is deleted.".format(name)}
        else:
            return {'message': "An item with name '{}' not exist.".format(name)}
 


class Items(Resource):
    TABLE_NAME = "items"
    #@jwt_required()
    def get(self):
        conn = sqlite3.connect('mydata.db')
        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        row = conn.cursor().execute(query).fetchall()
        conn.close()
        if row:
            return {'items': [{"name":i, "price":j} for i,j in row]}