from database.db import db
from bson import ObjectId
from datetime import datetime

comments_collection = db["comments"]


def create_comment(data):
    comment = {
        "post": ObjectId(data["post"]),
        "user": ObjectId(data["user"]),
        "text": data["text"],
        "parentComment": ObjectId(data["parentComment"]) if data.get("parentComment") else None,
        "createdAt": datetime.utcnow()
    }

    return comments_collection.insert_one(comment)


def get_comments_by_post(post_id):
    return list(
        comments_collection
        .find({"post": ObjectId(post_id)})
        .sort("createdAt", 1)
    )


def delete_comment(comment_id, user_id):
    return comments_collection.delete_one({
        "_id": ObjectId(comment_id),
        "user": ObjectId(user_id)
    })