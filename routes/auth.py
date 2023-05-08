from flask import Blueprint, jsonify, request
import jwt
from sqlalchemy import select
from connector import conn
from models.user import User
from werkzeug.security import check_password_hash
from routes.token import sec_keys
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    forms = request.form
    if "email" not in forms or "password" not in forms:
        return jsonify({"msg": "Failing to Authenticate"}), 401

    user = conn.session.scalars(select(User).where(
        User.email == forms["email"])).one()

    if not check_password_hash(user.password, forms["password"]):
        return jsonify({"msg": "Invalid Password"}), 401

    encode_jwt = jwt.encode(
        {"uid": user.uid, "email": user.email}, sec_keys, algorithm="HS256")
    return jsonify({"token": encode_jwt})
