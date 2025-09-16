from datetime import datetime, timedelta
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db, login_manager
from ..models import User, ApiKey
from . import auth_bp


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))


@auth_bp.post("/signup")
def signup():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "email and password required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already exists"}), 409
    user = User(email=email, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "email": user.email}), 201


@auth_bp.post("/apikeys")
def create_api_key():
    # Simple: allow email+password to create an API key in one request
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "email and password required"}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "invalid credentials"}), 401
    key_value = ApiKey.generate_key()
    api_key = ApiKey(user_id=user.id, key=key_value, expires_at=None)
    db.session.add(api_key)
    db.session.commit()
    return jsonify({"api_key": api_key.key}), 201


