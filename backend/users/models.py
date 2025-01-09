from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

print(uuid.uuid4())

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean, default=False)
    profile_is_admin_approved = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String)
    markdown = db.Column(db.Text, default="")
    uuid = db.Column(db.String(36), unique=True, default=str(uuid.uuid4()))
