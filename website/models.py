from . import db
from flask_login import UserMixin

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Integer)
    repeatCount = db.Column(db.Integer)

class BlockOfBlocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blocks = db.relationship("Block", backref="blockOfBlocks", lazy=True)
    isSet = db.Column(db.Boolean)

class TrainingSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blocksOfBlocks = db.relationship("BlockOfBlocks", backref="trainingSession", lazy=True)
    totalDistance = db.Column(db.Integer)
    hasSet = db.Column(db.Boolean)
    totalSetDistance = db.Column(db.Integer)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    trainingSessions = db.relationship("TrainingSession", backref="user", lazy=True)
