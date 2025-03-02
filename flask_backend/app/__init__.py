# Initialize Flask app and register blueprints
from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.routes import register_routes
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"




def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})  # Enable CORS if needed

    register_routes(app)  # Register all API routes
    # Setup Swagger UI
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
