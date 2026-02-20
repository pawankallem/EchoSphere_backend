from flask import Blueprint, request, jsonify
from utils.auth_middleware import jwt_required
from models.comment_model import create_comment, get_comments_by_post, delete_comment
from utils.user_preview import get_user_preview

comment_bp = Blueprint("comments", __name__)

@comment_bp.post("/send")
@jwt_required
def add_comment():
    data = request.json

    if not data.get("post") or not data.get("text"):
        return jsonify({"error": "Post ID and text required"}), 400

    comment_data = {
        "post": data["post"],
        "user": request.user_id,
        "text": data["text"],
        "parentComment": data.get("parentComment")
    }

    result = create_comment(comment_data)

    return jsonify({
        "message": "Comment added",
        "comment_id": str(result.inserted_id)
    }), 201


@comment_bp.route("/<post_id>", methods=["GET"])
def get_comments(post_id):
    comments = get_comments_by_post(post_id)
    enriched = []

    for c in comments:
        enriched.append({
            "_id": str(c["_id"]),
            "text": c["text"],
            "user": get_user_preview(c["user"]),
            "parentComment": str(c["parentComment"]) if c["parentComment"] else None,
            "createdAt": c["createdAt"]
        })

    return jsonify(enriched), 200


@comment_bp.route("/<comment_id>", methods=["DELETE"])
@jwt_required
def remove_comment(comment_id):
    delete_comment(comment_id, request.user_id)
    return jsonify({"message": "Comment deleted"})