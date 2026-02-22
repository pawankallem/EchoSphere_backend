from database.db import db
from bson import ObjectId
from datetime import datetime
from models.notification_model import create_notification

posts_collection = db["posts"]
comments_collection = db["comments"]


def create_comment(data):
    comment = {
        "post": ObjectId(data["post"]),
        "user": ObjectId(data["user"]),
        "text": data["text"],
        "parentComment": ObjectId(data["parentComment"]) if data.get("parentComment") else None,
        "createdAt": datetime.utcnow()
    }

    result = comments_collection.insert_one(comment)

    posts_collection.update_one(
        {"_id": ObjectId(data["post"])},
        {"$inc": {"commentsCount": 1}}
    )

    post = posts_collection.find_one({"_id": ObjectId(data["post"])})

    if str(post["author"]) != str(data["user"]):
        create_notification({
            "recipient": post["author"],
            "sender": data["user"],
            "type": "comment",
            "post": data["post"],
            "message": "commented on your post"
        })

    return result


def get_comments_by_post(post_id):
    return list(
        comments_collection
        .find({"post": ObjectId(post_id)})
        .sort("createdAt", 1)
    )


def delete_comment(comment_id, user_id):
    comment = comments_collection.find_one({
        "_id": ObjectId(comment_id),
        "user": ObjectId(user_id)
    })

    if comment:
        comments_collection.delete_one({"_id": comment["_id"]})

        posts_collection.update_one(
            {"_id": comment["post"]},
            {"$inc": {"commentsCount": -1}}
        )