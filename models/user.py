from connector import conn


class User(conn.Model):

    __tablename__ = "user"

    id = conn.Column(conn.Integer, primary_key=True)
    uid = conn.Column(conn.String(225), unique=True, nullable=False)
    name = conn.Column(conn.String(225),  nullable=False)
    email = conn.Column(conn.String(225), unique=True, nullable=False)
    password = conn.Column(conn.String(225), unique=True, nullable=False)
    avatar = conn.Column(conn.String(225),  nullable=False)
