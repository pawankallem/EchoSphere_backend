from database.db import db
from bson import ObjectId
from datetime import datetime

posts_collection = db["posts"]

def create_post(data):
    post = {
        "author": ObjectId(data["author"]),
        "caption": data.get("caption", ""),
        "image": data.get("image"),
        "video": data.get("video"),
        "likes": [],
        "savedBy": [],
        "commentsCount": 0,
        "createdAt": datetime.utcnow()
    }

    return posts_collection.insert_one(post)


def get_all_posts():
    return list(posts_collection.find().sort("createdAt", -1))


def get_post_by_id(post_id):
    return posts_collection.find_one({"_id": ObjectId(post_id)})


def like_post(post_id, user_id):
    return posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$addToSet": {"likes": ObjectId(user_id)}}
    )

def save_post(post_id, user_id):
    return posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$addToSet": {"savedBy": ObjectId(user_id)}}
    )

def get_posts_by_user_id(user_id):
    return list(posts_collection.find({"author": ObjectId(user_id)}).sort("createdAt", -1))

def toggle_like(post_id, user_id):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})

    if ObjectId(user_id) in post.get("likes", []):
        return posts_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$pull": {"likes": ObjectId(user_id)}}
        )
    else:
        return posts_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$addToSet": {"likes": ObjectId(user_id)}}
        )
    
def toggle_save(post_id, user_id):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})

    if ObjectId(user_id) in post.get("savedBy", []):
        return posts_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$pull": {"savedBy": ObjectId(user_id)}}
        )
    else:
        return posts_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$addToSet": {"savedBy": ObjectId(user_id)}}
        )