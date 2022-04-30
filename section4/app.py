from functools import lru_cache
from xmlrpc.client import Boolean
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from typing import *

app = Flask(__name__)
app.secret_key = "vald3000"
api = Api(app)
jwt = JWT(app, authenticate, identity)

items = [
    {
        "name": "test",
        "price": 3.33
    }
]

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float,required=True,help="This field cannot be left blank!")

    @staticmethod
    def search(name, data) -> Boolean:
        return True if [i for i in data if i["name"] == name] else False
        

    def get(self, name):
        if self.search(name, items):
            return {"items": [i for i in items if i["name"] == name]}, 200
        else:
            return {"massage": f"{name} wasn't found!"}, 404
 
    def post(self, name):
        if self.search(name,items):
            print(name,items)
            return {"Item": f"{name} is already exists"}, 400
        else:
            new_item = {
                "name": name,
                "price": Item.parser.parse_args()["price"]
            }
            items.append(new_item)
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

api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items,"/items")

if __name__ == "__main__":
    app.run()
