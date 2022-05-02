from flask import Flask,jsonify
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity as identity_function
from resources.users import Register
from resources.items import Item, Items
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "skdnmlcnevnle332d2"
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity_function)

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
     })

@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
     }), error.status_code

api = Api(app)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items,"/items")
api.add_resource(Register,"/register")

if __name__ == "__main__":
    app.run()
