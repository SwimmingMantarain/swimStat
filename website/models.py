from . import db
from flask_login import UserMixin

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Integer)
    repeatCount = db.Column(db.Integer)
    stroke = db.Column(db.String(30))
    exercise = db.Column(db.String(200))
    block_of_blocks_id = db.Column(db.Integer, db.ForeignKey('block_of_blocks.id'), nullable=True)

class BlockOfBlocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    blocks = db.relationship('Block', backref='block_of_blocks', lazy=True)
    training_session_id = db.Column(db.Integer, db.ForeignKey('training_session.id'), nullable=True)
    is_set = db.Column(db.Boolean, default=False)

class TrainingSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    blocks = db.relationship('BlockOfBlocks', backref='training_session', lazy=True)
    total_distance = db.Column(db.Integer)
    contains_set = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    training_sessions = db.relationship('TrainingSession', backref='user', lazy=True)
