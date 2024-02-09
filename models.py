from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UsersDB(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.Text, nullable=False)
