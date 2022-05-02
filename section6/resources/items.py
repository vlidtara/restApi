from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from modules.items import ItemModule
from typing import *

class Item(Resource):


    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float,required=True,help="This field cannot be left blank!")
    

    #@jwt_required()
    def get(self, name):
        item = ItemModule.find_by_user(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


    #@jwt_required()
    def post(self, name):
        if ItemModule.find_by_user(name):
            return {'message': "An item with name '{}' already exists.".format(name)}
        else:
            data = Item.parser.parse_args()
            new_item = ItemModule(name, data["price"]) 
            try:
                new_item.insert()
            except:
                return {"message": "An error occurred inserting the item."}, 500
            return new_item.json(), 201
            
    def put(self, name):
        data = Item.parser.parse_args()
        new_item = ItemModule(name, data["price"])       
        if ItemModule.find_by_user(name):
            try:
                new_item.update()
            except:
                return {"message": "An error occurred updating the item."}, 500
            return {'message': "An item with name '{}' is updated.".format(name)}, 201
        else:
            try:
                new_item.insert()
            except:
                return {"message": "An error occurred inserting the item."}, 500
            return {'message': "An item with name '{}' is created.".format(name)}, 201

    #@jwt_required()
    def delete(self, name):
        if ItemModule.find_by_user(name):
            ItemModule.delete_by_user(name)
            return {'message': "An item with name '{}' is deleted.".format(name)}
        else:
            return {'message': "An item with name '{}' not exist.".format(name)}, 404
 

class Items(Resource):

    #@jwt_required()
    def get(self):
        row = ItemModule.select_all()
        if row:
            return {'items': [{"name":i, "price":j} for i,j in row]}