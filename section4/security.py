from users import Users

db_users = [
    Users(1,"vlad","12345")
]

username_mapping = {u.username: u for u in db_users}
userid_mapping = {u.id: u for u in db_users}

def authenticate(username,password):
    user = username_mapping.get(username, None)
    if user and user.password == password: return user

def identity(payload):
    user_id = payload["identity"]
    return userid_mapping.get(user_id,None)

