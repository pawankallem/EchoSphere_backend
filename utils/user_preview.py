from database.db import users_collection
from bson import ObjectId

def get_user_preview(user_id):
    user = users_collection.find_one(
        {"_id": ObjectId(user_id)},
        {"name": 1, "username": 1, "avatar": 1}
    )

    if not user:
        return None

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "username": user["username"],
        "avatar": user.get("avatar")
    }