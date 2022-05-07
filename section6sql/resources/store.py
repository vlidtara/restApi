from flask_restful import Resource
from modules.store import StoreModule


class Store(Resource):

    def get(self, name):
        store = StoreModule.find_by_name(name)
        if store:
            return store.json()
        return {'massage': 'Store not found'}, 404

    def post(self, name):
        store = StoreModule.find_by_name(name)
        if store:
            return {'massage': 'Store with the {} alredy exisist'.format(name)}, 400
        else:
            store = StoreModule(name)
            try:
                store.save_to_db()
                return {'massage': 'Store {} is created'.format(name)}
            except:
                return {'massage': 'An Error while creating the store {}'.format(name)}, 500

    def delet(self, name):
        store = StoreModule.find_by_name(name)
        if store:
            try:
                store.delete_from_db(name)
                return {'massage': 'The store {} is deleted'.format(name)}
            except:
                return {'massage': 'An Error while deleting the store {}'.format(name)}, 500
        else:
            return {'massage': "The store {} dosen't exisist".format(name)}, 500


class StoreList(Resource):
    def get(self):
        store = StoreModule.select_all()
        if store:
            return {'Stores': [i.json() for i in store]}
        else:
            return {"Stores": []}
