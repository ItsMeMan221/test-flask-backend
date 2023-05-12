from flask import Flask, jsonify
from routes.users import users_bp
from connector import conn
from routes.auth import auth_bp
from routes.errors import error_bp
from datetime import timedelta
from tokenutils import jwt


app = Flask(__name__)

# Need Change Config
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost:3306/test-flask-db"

app.config['JWT_SECRET_KEY'] = "6dcc9951a30568db5f221e3ee7e8c455"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(hours=1)

conn.app = app
conn.init_app(app)
jwt.init_app(app)

app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(error_bp)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify("OK")


if (__name__ == "__main__"):
    app.run(host="127.0.0.1", debug=True)
