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
            conn = sqlite3.connect('mydata.db')
            query = "INSERT INTO {table} VALUES(?,?)".format(table=self.TABLE_NAME)
            conn.cursor().execute(query,(new_item["name"], new_item["price"]))
            conn.commit()
            conn.close()
            return new_item, 201
            
    def put(self, name):
        request_data = Item.parser.parse_args()
        if self.search(name,items):
            [i.update({"price": request_data["price"]}) for i in items if i["name"] == name ]
            return {"massage": f'the price {request_data["price"]} was changed for {name}'}, 202
        else:
            new_item = {
                "name": name,
                "price":request_data["price"]
            }
            items.append(new_item)
            return {"massage": f"{name} was added"}, 201
   
    #@jwt_required()
    def delete(self, name):
        if self.search(name,items):
            [items.pop(i) for i,val in enumerate(items) if val["name"] == name]
            return {"item": f"{name} was deleted!"}

class Items(Resource):
    #@jwt_required()
    def get(self):
        return items