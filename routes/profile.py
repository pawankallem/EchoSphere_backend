from flask import Blueprint, request, jsonify
from utils.auth_middleware import jwt_required
from models.user_model import get_user_by_id, update_user
from models.post_model import get_posts_by_user_id 

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("", methods=["GET"])
@jwt_required
def get_profile():
    try:
        user = get_user_by_id(request.user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        posts = get_posts_by_user_id(user["_id"])
        enriched_posts = []

        for post in posts:
            likes = post.get("likes", [])
            saved = post.get("savedBy", [])

            enriched_posts.append({
                "_id": str(post["_id"]),
                "caption": post.get("caption"),
                "image": post.get("image"),
                "video": post.get("video"),

                "author": str(post["author"]),

                "likesCount": len(likes),
                "savedCount": len(saved),
                "commentsCount": post.get("commentsCount", 0),

                "likes": request.user_id in [str(u) for u in likes],
                "savedBy": request.user_id in [str(u) for u in saved],
                "likedBy": [str(u) for u in likes],
                "savedByUsers": [str(u) for u in saved],

                "createdAt": str(post.get("createdAt"))
            })

        return jsonify({
            "user": {
                "id": str(user["_id"]),
                "name": user["name"],
                "username": user["username"],
                "email": user["email"],
                "avatar": user.get("avatar"),
                "bio": user.get("bio"),
                "location": user.get("location"),
                "website": user.get("website"),
                "followers": [str(f) for f in user.get("followers", [])],
                "following": [str(f) for f in user.get("following", [])]
            },
            "posts": enriched_posts
        }), 200

    except Exception as e:
        print("Error fetching profile:", e)
        return jsonify({"error": "Server error"}), 500
    


@profile_bp.route("/update", methods=["PUT"])
@jwt_required
def update_profile():
    try:
        data = request.json

        update_user(request.user_id, data)

        return jsonify({"message": "Profile updated successfully"}), 200

    except Exception as e:
        print("Profile update error:", e)
        return jsonify({"error": "Server error"}), 500