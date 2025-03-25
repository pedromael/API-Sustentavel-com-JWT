from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.database import get_db

actions_bp = Blueprint('actions', __name__)

@actions_bp.after_request
def apply_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@actions_bp.route('/', methods=['POST'])
@jwt_required()
def create_action():
    data = request.get_json()
    
    if not data or not all(key in data for key in ('title', 'description', 'category', 'points', 'user_id')):
        return jsonify({"message": "Dados incompletos"}), 422

    title = data.get('title')
    description = data.get('description')
    category = data.get('category')
    points = data.get('points')
    user_id = data.get('user_id')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO actions (title, description, category, points, user_id, data) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", 
                   (title, description, category, points, user_id))
    db.commit()

    return jsonify({"message": "Ação cadastrada com sucesso!"}), 201

@actions_bp.route('/', methods=['GET'])
@jwt_required()
def get_actions():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT actions.title, actions.description, actions.category, actions.points, actions.data, users.name, users.id
        FROM actions 
        JOIN users ON actions.user_id = users.id
    """)
    actions = cursor.fetchall()

    actions_list = [{"title": action[0], "description": action[1], "category": action[2], "points": action[3], "data": action[4], "user_name": action[5], "id": action[6] } for action in actions]

    return jsonify(actions_list), 200

@actions_bp.route('/<int:action_id>', methods=['DELETE'])
@jwt_required()
def delete_action(action_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM actions WHERE id = ?", (action_id,))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"message": "Ação não encontrada"}), 404

    return jsonify({"message": "Ação eliminada com sucesso!"}), 200