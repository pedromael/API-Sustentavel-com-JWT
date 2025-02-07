from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Action

actions_bp = Blueprint("actions", __name__)

@actions_bp.route("/", methods=["POST"])
@jwt_required()
def create_action():
    user_id = get_jwt_identity()
    data = request.get_json()
    action = Action(title=data["title"], description=data["description"], category=data["category"], points=data["points"], user_id=user_id)
    db.session.add(action)
    db.session.commit()
    return jsonify({"message": "Ação registrada!"}), 201

@actions_bp.route("/", methods=["GET"])
def list_actions():
    actions = Action.query.all()
    return jsonify([{"id": a.id, "title": a.title, "description": a.description, "category": a.category, "points": a.points} for a in actions])
