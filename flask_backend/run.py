from app import create_app
from flask_cors import CORS  # Import CORS
from app.routes.popi import popi_bp
from app.routes.dogparks import dogparks_bp

app = create_app()
""" CORS(popi_bp, resources={r"/*": {"origins": "*", "allow_headers": "*", "methods": ["GET", "POST", "OPTIONS"]}})
 """
""" # Register Blueprints
app.register_blueprint(popi_bp)
app.register_blueprint(dogparks_bp)
 """

if __name__ == "__main__":
    app.run(debug=True)
