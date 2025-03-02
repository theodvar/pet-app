from flask import Blueprint, jsonify, request
from app.services.dogparks_service import get_all_dogparks, get_dogpark_by_id, create_dogpark, update_dogpark, delete_dogpark


dogparks_bp = Blueprint("dogparks", __name__, url_prefix="/api/dogparks")

@dogparks_bp.route("/", methods=["GET"], strict_slashes=False)
def get_all():
    return get_all_dogparks()

@dogparks_bp.route("/<int:id>", methods=["GET"], strict_slashes=False)
def get_by_id(id):
    return get_dogpark_by_id(id)

@dogparks_bp.route("/", methods=["POST"], strict_slashes=False)
def create():
    return create_dogpark(request.get_json())

@dogparks_bp.route("/<int:id>", methods=["PUT"], strict_slashes=False)
def update(id):
    return update_dogpark(id, request.get_json())

@dogparks_bp.route("/<int:id>", methods=["DELETE"], strict_slashes=False)
def delete(id):
    return delete_dogpark(id)
