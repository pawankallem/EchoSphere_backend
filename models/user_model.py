from database.db import users_collection
from bson import ObjectId
from datetime import datetime

def create_user(data):
    user = {
        "name": data["name"],
        "username": data["username"],
        "email": data["email"],
        "password": data["password"],

        "avatar": "",
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


def update_user(user_id, data):
    update_fields = {}

    allowed_fields = ["name", "avatar", "bio", "location", "website"]

    for field in allowed_fields:
        if field in data:
            update_fields[field] = data[field]

    return users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_fields}
    )