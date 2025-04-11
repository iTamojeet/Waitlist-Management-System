import os
import logging
from datetime import datetime, timedelta
import json
from flask import Flask, render_template, request, session, redirect, url_for
from markupsafe import Markup

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Import database
from database import db, init_db

# Create Flask app
app = Flask(__name__)

# Configure app
app.config.from_object('config.DevelopmentConfig')
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')

# Initialize database
init_db(app)

# Utility functions
def to_datetime(value):
    """Convert a string to datetime object"""
    if isinstance(value, datetime):
        return value
    try:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return None

def escapejs(value):
    """Escape JSON for safe use in JavaScript"""
    return Markup(json.dumps(value))

# Register the to_datetime function as a Jinja2 filter
app.jinja_env.filters['to_datetime'] = to_datetime

# Register the escapejs function as a Jinja2 filter
app.jinja_env.filters['escapejs'] = escapejs

# Template context processors
@app.context_processor
def utility_processor():
    """Add utility functions and objects to template context"""
    return {
        'now': datetime.utcnow(),
        'timedelta': timedelta,
        'to_datetime': to_datetime
    }

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('error.html', error_code=404, message="Page Not Found"), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('error.html', error_code=500, message="Server Error"), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}, 200

# Import routes
import routes