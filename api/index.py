from flask import Flask
from routes.auth_routes import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix="/api/auth")

@app.route("/")
def home():
    return {"status": "API running"}

# Vercel handler
def handler(request, context):
    return app(request.environ, start_response=context.start_response)

