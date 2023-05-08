from flask import Flask, jsonify
from routes.users import users_bp
from connector import conn
from routes.auth import auth_bp
from routes.errors import error_bp

app = Flask(__name__)

# Need Change Config
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost:3306/test-flask-db"

app.config["SECRET_KEY"] = "19eb9aeb4516b29dfd246d2d72f38a9a"


app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(error_bp)

conn.app = app
conn.init_app(app)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify("OK")


if (__name__ == "__main__"):
    app.run(host="127.0.0.1", debug=True)
