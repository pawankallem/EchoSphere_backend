from flask import Flask
from routes.auth_routes import auth_bp

app = Flask(__name__)

# register routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")

@app.route("/")
def home():
    return {"status": "EchoSphere backend running"}
