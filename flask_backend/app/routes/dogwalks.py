from flask import Blueprint, jsonify, request
from app.services.dogwalks_service import get_all_dogwalks, get_dogwalk_by_id, create_dogwalk, update_dogwalk, delete_dogwalk

dogwalks_bp = Blueprint("dogwalks", __name__, url_prefix="/api/dogwalks")

@dogwalks_bp.route("/", methods=["GET"], strict_slashes=False)
def get_all():
    return get_all_dogwalks()

@dogwalks_bp.route("/<int:id>", methods=["GET"], strict_slashes=False)
def get_by_id(id):
    return get_dogwalk_by_id(id)

@dogwalks_bp.route("/", methods=["POST"], strict_slashes=False)
def create():
    return create_dogwalk(request.get_json())

@dogwalks_bp.route("/<int:id>", methods=["PUT"], strict_slashes=False)
def update(id):
    return update_dogwalk(id, request.get_json())

@dogwalks_bp.route("/<int:id>", methods=["DELETE"], strict_slashes=False)
def delete(id):
    return delete_dogwalk(id)
