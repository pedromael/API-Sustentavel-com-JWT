from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from ..models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")
    
    new_user = User(username=data["username"], email=data["email"], password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuário registrado com sucesso!"}), 201
    except IntegrityError:
        return jsonify({"message": "Usuário ou email já existem"}), 400

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Credenciais inválidas"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token})
