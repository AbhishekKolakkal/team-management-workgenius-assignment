from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
from .database import db


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, ForeignKey('users.id'))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    teams = db.relationship('Team', backref='users', lazy=True)
