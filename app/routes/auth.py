from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.database import get_db

auth_bp = Blueprint("auth", __name__)

# Middleware para adicionar cabeçalhos CORS
@auth_bp.after_request
def apply_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"message": "Email já cadastrado"}), 400

    cursor.execute("INSERT INTO users (email, password, name) VALUES (?, ?, ?)", 
                   (email, generate_password_hash(password), name))
    db.commit()

    user_id = cursor.lastrowid

    return jsonify({"message": "Usuário cadastrado com sucesso!", "user_id": user_id}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user and check_password_hash(user[2], password):
        access_token = create_access_token(identity=str(user[0]))
        return jsonify(access_token=access_token, user_id=user[0]), 200
    else:
        return jsonify({"message": "Credenciais inválidas"}), 401

