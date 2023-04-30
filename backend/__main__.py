from flask import jsonify, request
from backend import app_create

users = []
app = app_create()


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify("OK")


@app.route("/user", methods=["GET"])
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


@app.route("/user", methods=["POST"])
def addUser():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user = {
            'email': email,
            'name': name
        }
        users.append(user)
        return jsonify(
            {
                'msg': "User {} has been added".format(name)
            }
        ), 201


@app.route("/user", methods=["PUT"])
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


@app.route("/user", methods=["DELETE"])
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


if (__name__ == "__main__"):
    app.run(host="127.0.0.1", debug=True)
