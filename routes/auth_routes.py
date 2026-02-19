from flask import Blueprint, request, jsonify
from models.user_model import create_user, find_by_email, find_by_username, get_user_by_id
from utils.password_utils import hash_password, check_password
from utils.jwt_handler import generate_token, decode_token
from utils.auth_middleware import jwt_required


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    required_fields = ["fullname", "username", "email", "password"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    if find_by_email(data["email"]):
        return jsonify({"error": "Email already exists"}), 400

    if find_by_username(data["username"]):
        return jsonify({"error": "Username already exists"}), 400

    hashed_pw = hash_password(data["password"])

    user_data = {
        "name": data["fullname"],
        "username": data["username"],
        "email": data["email"],
        "password": hashed_pw
    }

    result = create_user(user_data)

    return jsonify({
        "message": "User created successfully",
        "user_id": str(result.inserted_id)
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = find_by_email(data.get("email"))

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password(data["password"], user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user["_id"])

    return jsonify({
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "username": user["username"],
            "email": user["email"],
            "avatar": user["avatar"]
        }
    })


@auth_bp.route("/me", methods=["GET"])
@jwt_required
def get_current_user():

    try:
        user = get_user_by_id(request.user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "id": str(user["_id"]),
            "name": user["name"],
            "username": user["username"],
            "email": user["email"],
            "avatar": user.get("avatar"),
            "bio": user.get("bio"),
            "location": user.get("location"),
            "website": user.get("website"),
            "followers": user.get("followers", []),
            "following": user.get("following", [])
        }), 200

    except Exception as e:
        return jsonify({"error": "Invalid or expired token"}), 401
