from resources.users import Users
from hmac import compare_digest


def authenticate(username,password):
    user = Users.find_by_username(username)
    if user and compare_digest(user.password,password): return user

def identity(payload):
    user_id = payload["identity"]
    return Users.find_by_id(user_id)
