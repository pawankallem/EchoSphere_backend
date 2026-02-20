from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.post_routes import post_bp

from config import PORT, FRONTEND_URL

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": FRONTEND_URL}})

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(post_bp, url_prefix="/api/posts")

@app.route("/")
def home():
    return {"message": "API running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)