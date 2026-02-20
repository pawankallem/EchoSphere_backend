from flask import Blueprint, request, jsonify
from utils.auth_middleware import jwt_required
from models.post_model import create_post, get_all_posts, like_post, save_post
from utils.user_preview import get_user_preview

post_bp = Blueprint("posts", __name__)


@post_bp.post("/create")
@jwt_required
def create_new_post():
    data = request.json

    if not data.get("image") and not data.get("video"):
        return jsonify({"error": "Post must include image or video"}), 400

    post_data = {
        "author": request.user_id,
        "caption": data.get("caption"),
        "image": data.get("image"),
        "video": data.get("video")
    }

    result = create_post(post_data)

    return jsonify({
        "message": "Post created",
        "post_id": str(result.inserted_id)
    }), 201


@post_bp.get("/get")
@jwt_required
def get_posts():
    posts = get_all_posts()
    enriched_posts = []

    for post in posts:
        likes = post.get("likes", [])
        saved = post.get("savedBy", [])

        enriched_posts.append({
            "_id": str(post["_id"]),
            "caption": post.get("caption"),
            "image": post.get("image"),
            "video": post.get("video"),

            "author": get_user_preview(post["author"]),

            "likesCount": len(likes),
            "savedCount": len(saved),
            "commentsCount": post.get("commentsCount", 0),

            "likes": request.user_id in [str(u) for u in likes],
            "savedBy": request.user_id in [str(u) for u in saved],

            "createdAt": post["createdAt"]
        })

    return jsonify(enriched_posts), 200

@post_bp.route("/<post_id>/like", methods=["PUT"])
@jwt_required
def like(post_id):
    like_post(post_id, request.user_id)
    return jsonify({"message": "Post liked"})



@post_bp.route("/<post_id>/save", methods=["PUT"])
@jwt_required
def save(post_id):
    save_post(post_id, request.user_id)
    return jsonify({"message": "Post saved"})