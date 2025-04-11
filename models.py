"""Database models for the application"""
import random
import string
from datetime import datetime

from database import db
from sqlalchemy.orm import validates


def generate_referral_code(length=8):
    """Generate a unique referral code for new subscribers
    
    Args:
        length (int): Length of the referral code
        
    Returns:
        str: A random alphanumeric referral code
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


class Subscriber(db.Model):
    """Model for waitlist subscribers"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(50), nullable=True)
    newsletter = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50), nullable=True)
    referral_code = db.Column(db.String(50), unique=True, nullable=True)
    
    def __init__(self, **kwargs):
        """Initialize a new subscriber
        
        Generate a unique referral code on initialization
        """
        super(Subscriber, self).__init__(**kwargs)
        # Generate a unique referral code
        if not self.referral_code:
            self.referral_code = generate_referral_code()
    
    @validates('email')
    def validate_email(self, key, email):
        """Validate email format"""
        if '@' not in email or '.' not in email:
            raise ValueError("Invalid email address")
        return email

    def __repr__(self):
        """String representation of the subscriber"""
        return f'<Subscriber {self.email}>'