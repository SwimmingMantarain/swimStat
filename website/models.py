from . import db
from flask_login import UserMixin

# Block Model: Stores information about a block of a training session
class Block(db.Model):
    """
    Model to store information about a block of a training session
    """
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Integer)
    repeatCount = db.Column(db.Integer)
    stroke = db.Column(db.String(30))
    exercise = db.Column(db.String(200))
    # Foreign key to BlockOfBlocks table
    block_of_blocks_id = db.Column(db.Integer, 
                                   db.ForeignKey('block_of_blocks.id'), 
                                   nullable=True)


# BlockOfBlocks Model: Stores information about a group of blocks in a training session
class BlockOfBlocks(db.Model):
    """
    Model to store information about a group of blocks in a training session
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    # One-to-many relationship with the Block model
    blocks = db.relationship('Block', backref='block_of_blocks', lazy=True)
    # Foreign key to TrainingSession table
    training_session_id = db.Column(db.Integer, 
                                     db.ForeignKey('training_session.id'), 
                                     nullable=True)
    is_set = db.Column(db.Boolean, default=False)


# TrainingSession Model: Stores information about a training session
class TrainingSession(db.Model):
    """
    Model to store information about a training session
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    # One-to-many relationship with the BlockOfBlocks model
    blocks = db.relationship('BlockOfBlocks', backref='training_session', lazy=True)
    total_distance = db.Column(db.Integer)
    contains_set = db.Column(db.Boolean, default=False)
    set_distance = db.Column(db.Integer)
    # Foreign key to User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# User Model: Stores information about a user
class User(db.Model, UserMixin):
    """
    Model to store information about a user
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    # One-to-many relationship with the TrainingSession model
    training_sessions = db.relationship('TrainingSession', 
                                         backref='user', 
                                         lazy=True)

