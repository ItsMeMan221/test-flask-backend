import os
import secrets
from flask import Blueprint, jsonify, request
from sqlalchemy import delete, insert, select, update
from models.user import User
from module.uploadImg import bucket
from connector import conn
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required

users_bp = Blueprint("user", __name__, url_prefix="/user")


@users_bp.route("", methods=["GET"])
@jwt_required()
def get_user():
    users = conn.session.scalars(select(User)).all()

    return jsonify([{"id": user.id, "uid": user.uid, "name": user.email, "avatar": user.avatar} for user in users])


@users_bp.route("/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = conn.session.scalars(select(User).where(User.id == user_id)).one()

    return jsonify({"id": user.id, "uid": user.uid, "name": user.email, "avatar": user.avatar})


@users_bp.route("", methods=["POST"])
def add_user():
    forms = request.form
    uid = secrets.token_hex(16)

    # Processing Image
    image_file = request.files['avatar']
    image_ext = os.path.splitext(image_file.filename)[1]
    if image_ext != '.jpg' and image_ext != '.jpeg' and image_ext != '.png':
        return jsonify({
            'msg': 'image format must be jpg or png or jpeg'
        }), 400
    check_email = conn.session.scalars(
        select(User).where(User.email == forms["email"])).one_or_none()
    if check_email:
        return jsonify({'msg': 'Gmail already been taken'})
    image_file.filename = secrets.token_hex(16) + image_ext
    image = bucket.blob('avatar/' + image_file.filename)
    image.upload_from_file(image_file, content_type="image")
    public_url = image.public_url

    # Insert to database
    conn.session.execute(insert(User).values(
        email=forms['email'], password=generate_password_hash(forms['password']), uid=uid, avatar=public_url, name=forms['name']))
    conn.session.commit()

    # Return a msg
    return jsonify(
        {
            "msg": f"User {forms['name']} is added"
        }
    )


@users_bp.route("/<uid>", methods=["PUT"])
def edit_user(uid):
    forms = request.form
    image_file = request.files['avatar']
    image_ext = os.path.splitext(image_file.filename)[1]
    if image_ext != '.jpg' and image_ext != '.jpeg' and image_ext != '.png':
        return jsonify({
            'msg': 'image format must be jpg or png or jpeg'
        }), 400
    image_file.filename = secrets.token_hex(16) + image_ext
    image = bucket.blob('avatar/' + image_file.filename)
    image.upload_from_file(image_file, content_type="image")
    public_url = image.public_url

    conn.session.execute(update(User).where(User.uid == uid).values(
        email=forms['email'], password=generate_password_hash(forms['password']), avatar=public_url, name=forms['name']))
    conn.session.commit()
    return jsonify({
        "msg": "User has been updated"
    })


@users_bp.route("/<uid>", methods=["DELETE"])
def delete_user(uid):
    conn.session.execute(delete(User).where(User.uid == uid))
    conn.session.commit()
    return jsonify({
        "msg": "User has been deleted"
    })
