from database.db import users_collection
from bson import ObjectId
from datetime import datetime

def create_user(data):
    user = {
        "name": data["name"],
        "username": data["username"],
        "email": data["email"],
        "password": data["password"],

        "avatar": "https://i.pravatar.cc/150",
        "bio": "",
        "location": "",
        "website": "",

        "followers": [],
        "following": [],

        "createdAt": datetime.utcnow()
    }

    return users_collection.insert_one(user)

def find_by_email(email):
    return users_collection.find_one({"email": email})

def find_by_username(username):
    return users_collection.find_one({"username": username})

def get_user_by_id(user_id):
    return users_collection.find_one({"_id": ObjectId(user_id)})
