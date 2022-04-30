import json
from unicodedata import name
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        "name": "Electro",
        "items": [
            {
                "name": "MacPook",
                "price": 3000
            }
        ]
    }
]

@app.route("/")
def home():
    return render_template("index.html")
    return "Hi, it is a Home page of our store"



#get /store/<name> data: {name :}
@app.route("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify(store)
    
    return jsonify({"massage": f"Store with name {name} not found!"})

#get /store
@app.route("/store")
def list_store():
    return jsonify({"Stores": stores})

    
#get /store/<name>/item data: {name :}
@app.route("/store/<string:name>/item")
def get_store_item(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items": store["items"]})
    return jsonify({"massage": f"Store with name {name} not found!"})


# @app.route("/store" , methods=["POST"])
# def create_store():
#     request_data = request.get_json()
#     new_store = {
#         "name": request_data["name"],
#          "items": []
#     }
#     stores.append(new_store)
#     return jsonify(new_store)

#post /store data: {name :}
@app.route("/store", methods=["POST"])
def create_store():
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items": []
    }
    stores.append(new_store)
    return jsonify(new_store)



#post /store/<name> data: {name :}
@app.route("/store/<string:name>/item", methods=["POST"])
def create_store_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {
                "name": request_data["name"],
                "price": request_data["price"]
            }
            store["items"].append(new_item)
            return jsonify(store)
    return jsonify({"massage": f"Store with name {name} not found!"})

if __name__ == "__main__":
    app.run(port=5000)

