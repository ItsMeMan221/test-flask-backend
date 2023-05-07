

from flask import Blueprint, jsonify, request
from modules.uploadImg import bucket
import os
import secrets

users_bp = Blueprint("user", __name__, url_prefix="/user")
users = []


@users_bp.route("", methods=["GET"])
def getUser():
    if request.method == 'GET':
        name = request.args.get('name')
        if name:
            for item_list in users:
                if (item_list['name'] == name):
                    return jsonify({
                        'name': item_list['name'],
                        'email': item_list['email'],
                    }), 200
            return jsonify({'msg': 'User is not exist'})

        if users and not name:
            return jsonify(users)
        else:
            return jsonify({
                'msg': 'users is null'
            })


@users_bp.route("", methods=["POST"])
def addUser():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        images = request.files['avatar']
        image_ext = os.path.splitext(images.filename)[1]

        if image_ext != '.jpg' and image_ext != '.jpeg' and image_ext != '.png':
            return jsonify({
                'msg': 'image format must be jpg or png or jpeg'
            }), 400

        images.filename = secrets.token_hex(16) + image_ext
        image = bucket.blob('avatar/' + images.filename)
        image.upload_from_file(images, content_type="image")
        public_url = image.public_url
        user = {
            'email': email,
            'name': name,
            'avatar': public_url
        }
        users.append(user)
        return jsonify(
            {
                'msg': "User {} has been added with avatar {}".format(name, public_url)
            }
        ), 201


@users_bp.route("", methods=["PUT"])
def editUser():
    name = request.form['name']
    email = request.form['email']
    name_param = request.args.get('name_param')

    for item_list in users:
        if (item_list['name'] == name_param):
            item_list['name'] = name
            item_list['email'] = email
            return jsonify({
                'msg': "User {} has been changed to {}".format(name_param, name)
            }), 201
    return jsonify({
        "msg": "User {} is not exist".format(name_param)
    }), 400


@users_bp.route("", methods=["DELETE"])
def deleteUser():
    name = request.args.get('name')

    for item_list in users:
        if (item_list['name'] == name):
            users.remove(item_list)
            return jsonify({
                "msg": "User {} has been deleted".format(name)
            }), 201
    return jsonify({
        "msg": "User {} is not exist".format(name)
    }), 404
