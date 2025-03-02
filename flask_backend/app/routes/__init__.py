from app.routes.dogparks import dogparks_bp
from app.routes.dogwalks import dogwalks_bp
from app.routes.popi import popi_bp

def register_routes(app):
    app.register_blueprint(dogparks_bp)
    app.register_blueprint(dogwalks_bp)
    app.register_blueprint(popi_bp)
