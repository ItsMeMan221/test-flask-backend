from flask import Flask, jsonify, request
from routes.users import users_bp


app = Flask(__name__)
app.register_blueprint(users_bp)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify("OK")


if (__name__ == "__main__"):
    app.run(host="127.0.0.1", debug=True)
