from database.db import db
from bson import ObjectId
from datetime import datetime

notifications_collection = db["notifications"]


def create_notification(data):
    notification = {
        "recipient": ObjectId(data["recipient"]),
        "sender": ObjectId(data["sender"]),
        "type": data["type"],  # like, comment, follow, follow_accept etc.
        "post": ObjectId(data["post"]) if data.get("post") else None,
        "message": data.get("message", ""),
        "isRead": False,
        "createdAt": datetime.utcnow()
    }

    return notifications_collection.insert_one(notification)


def get_notifications(user_id):
    return list(
        notifications_collection
        .find({"recipient": ObjectId(user_id)})
        .sort("createdAt", -1)
    )


def mark_as_read(notification_id):
    return notifications_collection.update_one(
        {"_id": ObjectId(notification_id)},
        {"$set": {"isRead": True}}
    )


def mark_all_as_read(user_id):
    return notifications_collection.update_many(
        {"recipient": ObjectId(user_id), "isRead": False},
        {"$set": {"isRead": True}}
    )


def delete_notification(notification_id):
    return notifications_collection.delete_one(
        {"_id": ObjectId(notification_id)}
    )