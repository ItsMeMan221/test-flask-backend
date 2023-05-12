from flask import Blueprint, jsonify, request

from sqlalchemy import select
from connector import conn
from models.user import User
from werkzeug.security import check_password_hash

from sqlalchemy.orm.exc import NoResultFound

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    forms = request.json
    if "email" not in forms or "password" not in forms:
        return jsonify({"msg": "Failing to Authenticate"}), 400

    try:
        user = conn.session.scalars(select(User).where(
            User.email == forms["email"])).one()
        if not check_password_hash(user.password, forms["password"]):
            return jsonify({"msg": "Invalid Password"}), 401
        token = create_access_token(identity={'uid': user.uid})
        refresh_token = create_refresh_token(identity={'uid': user.uid})
        return jsonify({
            'act_token': token,
            'refresh_token': refresh_token,
        }), 200
    except NoResultFound:
        return jsonify({"msg": "No email found"})


@auth_bp.route("/refresh_token", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    curr_user = get_jwt_identity()
    access_token = create_access_token(identity=curr_user)
    return jsonify({'acc_token': access_token})


@auth_bp.route("/session", methods=['GET'])
@jwt_required()
def session():
    curr_user = get_jwt_identity()
    return jsonify({'uid': curr_user['uid']})
