from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()  # Create SQLAlchemy instance
DB_NAME = "database.db"  # Set database name

def create_app():
    """Create and configure Flask app."""
    app = Flask(__name__)  # Create Flask app instance
    app.config["SECRET_KEY"] = "qaplweiucalkjdsfhaloei"  # Set secret key for app
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"  # Set database uri
    db.init_app(app)  # Initialize SQLAlchemy with app

    login_manager = LoginManager()  # Create LoginManager instance
    login_manager.login_view = "auth.login"  # Set login view
    login_manager.init_app(app)  # Initialize LoginManager with app

    # Register blueprints
    from .views import views
    from .auth import auth
    from .training import training

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(training, url_prefix="/")

    from .models import Block, BlockOfBlocks, TrainingSession, User
    create_database(app)  # Create database if it doesn't exist

    @login_manager.user_loader
    def load_user(id):
        """Load user by ID."""
        return User.query.get(int(id))

    return app


def create_database(app):
    """Create database if it doesn't exist."""
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
