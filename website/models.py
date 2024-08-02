from . import db
from flask_login import UserMixin

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Integer)
    repeatCount = db.Column(db.Integer)
    stroke = db.Column(db.String(30))
    exercise = db.Column(db.String(200))

class BlockOfBlocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blocks = db.ForeignKey("Block")
    name = db.Column(db.String(150))

class TrainingSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    blocks = db.ForeignKey("BlockOfBlocks")

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    trainingSessions = db.ForeignKey("TrainingSession")
