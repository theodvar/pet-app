from flask import Blueprint, jsonify, request
from app.services.popi_service import get_all_points, get_point_by_id, insert_point_data, update_petpointofinterest, delete_petpointofinterest
from flask_cors import CORS  # Import CORS


popi_bp = Blueprint("petpointofinterest", __name__, url_prefix="/api/petpointofinterest")
# CORS(popi_bp)

# Enable CORS for this Blueprint


@popi_bp.route("/", methods=["GET"], strict_slashes=False)
def get_all():
    return get_all_points()

@popi_bp.route("/<int:id>", methods=["GET"], strict_slashes=False)
def get_by_id(id):
    return get_point_by_id(id)

@popi_bp.route("/", methods=["POST"], strict_slashes=False)
def create():
    return insert_point_data(request.get_json())

@popi_bp.route("/<int:id>", methods=["PUT"], strict_slashes=False)
def update(id):
    return update_petpointofinterest(id, request.get_json())

@popi_bp.route("/<int:id>", methods=["DELETE"], strict_slashes=False)
def delete(id):
    return delete_petpointofinterest(id)

