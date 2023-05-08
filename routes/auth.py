from flask import Blueprint, jsonify, request
import jwt
from sqlalchemy import select
from connector import conn
from models.user import User
from werkzeug.security import check_password_hash
from routes.token import sec_keys, token_auth
from sqlalchemy.orm.exc import NoResultFound
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    forms = request.json
    if "email" not in forms or "password" not in forms:
        return jsonify({"msg": "Failing to Authenticate"}), 401

    try:
        user = conn.session.scalars(select(User).where(
            User.email == forms["email"])).one()
        if not check_password_hash(user.password, forms["password"]):
            return jsonify({"msg": "Invalid Password"}), 401

        encode_jwt = jwt.encode(
            {"uid": user.uid, "email": user.email},
            sec_keys,
            algorithm="HS256")

        return jsonify({"token": encode_jwt})

    except NoResultFound:
        return jsonify({"msg": "No email found"})


@auth_bp.route("/session", methods=["GET"])
@token_auth.login_required
def session():
    current_user = token_auth.current_user()
    return jsonify(current_user)
