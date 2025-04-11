"""Database configuration for the application"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models"""
    pass


# Initialize SQLAlchemy without binding to app yet
db = SQLAlchemy(model_class=Base)


def init_db(app):
    """Initialize the database with the Flask app"""
    db.init_app(app)
    
    # Import models here to avoid circular imports
    from models import Subscriber  # noqa
    
    # Create tables
    with app.app_context():
        db.create_all()


def reset_db():
    """Drop and recreate all tables (useful for testing)"""
    with db.engine.connect() as connection:
        db.drop_all(bind=None, app=None)
        db.create_all(bind=None, app=None)