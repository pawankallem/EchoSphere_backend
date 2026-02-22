from flask import Blueprint, jsonify, request
from utils.auth_middleware import jwt_required
from models.notification_model import (
    get_notifications,
    mark_as_read,
    mark_all_as_read
)
from utils.user_preview import get_user_preview

notification_bp = Blueprint("notifications", __name__)


@notification_bp.get("/all")
@jwt_required
def fetch_notifications():
    notifications = get_notifications(request.user_id)

    enriched = []

    for n in notifications:
        enriched.append({
            "_id": str(n["_id"]),
            "type": n["type"],
            "message": n.get("message", ""),
            "sender": get_user_preview(n["sender"]),
            "post": str(n["post"]) if n.get("post") else None,
            "isRead": n["isRead"],
            "createdAt": n["createdAt"]
        })

    return jsonify(enriched), 200


@notification_bp.put("/read/<notification_id>")
@jwt_required
def read_notification(notification_id):
    mark_as_read(notification_id)
    return jsonify({"message": "Marked as read"})


@notification_bp.put("/read-all")
@jwt_required
def read_all_notifications():
    mark_all_as_read(request.user_id)
    return jsonify({"message": "All notifications marked as read"})