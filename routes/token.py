from flask import jsonify
from flask_httpauth import HTTPTokenAuth
from sqlalchemy import select
from connector import conn
import jwt

from models.user import User


token_auth = HTTPTokenAuth(scheme="Bearer")

sec_keys = "6dcc9951a30568db5f221e3ee7e8c455"


@token_auth.verify_token
def verify_token(token):
    try:
        decode_jwt = jwt.decode(token, sec_keys, algorithms=["HS256"])
    except Exception as err:
        return None
    user = conn.session.scalars(select(User).where(
        User.email == decode_jwt['email'])).one_or_none()
    if user:
        return decode_jwt
    return None


@token_auth.error_handler
def token_err():
    response = jsonify({"msg": "Invalid Token"})
    response.status_code = 401
    return response
