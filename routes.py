"""Application routes and views"""
from flask import render_template, request, redirect, url_for, flash, session, jsonify, Response
from sqlalchemy import func
from app import app, db
from models import Subscriber
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import csv
from datetime import timedelta, datetime

limiter = Limiter(get_remote_address, app=app)

@app.route('/')
def index():
    """Render the landing page"""
    # Get count of subscribers for the waitlist counter
    subscriber_count = db.session.query(func.count(Subscriber.id)).scalar()
    return render_template('index.html', subscriber_count=subscriber_count)


@app.route('/subscribe', methods=['POST'])
@limiter.limit("5 per minute")
def subscribe():
    """Handle the waitlist signup form submission"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        source = request.form.get('source')
        newsletter = request.form.get('newsletter') == 'yes'
        
        # Validate input data
        if not name or not email:
            # Flash error message
            flash('Please provide both name and email', 'danger')
            return redirect(url_for('index'))
        
        # Check if email already exists
        existing_subscriber = Subscriber.query.filter_by(email=email).first()
        if existing_subscriber:
            # Don't reveal that email is already registered for privacy reasons
            flash('Thank you for your interest! Check your email for confirmation.', 'info')
            return redirect(url_for('success'))
        
        # Create new subscriber
        try:
            subscriber = Subscriber(
                name=name,
                email=email,
                source=source,
                newsletter=newsletter,
                ip_address=request.remote_addr
            )
            db.session.add(subscriber)
            db.session.commit()
            
            # Save referral code in session for showing on success page
            session['referral_code'] = subscriber.referral_code
            
            return redirect(url_for('success'))
        except Exception as e:
            app.logger.error(f"Error creating subscriber: {str(e)}")
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('index'))


@app.route('/success')
def success():
    """Render the success page after successful signup"""
    # Get count of subscribers for the counter
    subscriber_count = db.session.query(func.count(Subscriber.id)).scalar()
    
    # Generate referral link
    referral_code = session.get('referral_code')
    referral_link = None
    if referral_code:
        referral_link = f"{request.url_root}?ref={referral_code}"
    
    return render_template('success.html', 
                          subscriber_count=subscriber_count,
                          referral_link=referral_link)


@app.route('/admin')
def admin_dashboard():
    """Admin dashboard for waitlist stats"""
    # Get query parameters for pagination and search
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_query = request.args.get('search', '', type=str)

    # Query subscribers with optional search
    query = Subscriber.query
    if search_query:
        query = query.filter(
            (Subscriber.email.ilike(f"%{search_query}%")) |
            (Subscriber.name.ilike(f"%{search_query}%"))
        )
    
    # Paginate results and sort by created_at in ascending order
    pagination = query.order_by(Subscriber.created_at.asc()).paginate(page=page, per_page=per_page)
    subscribers = pagination.items

    # Count total subscribers
    total_count = pagination.total

    # Calculate stats by source
    stats = []
    sources = {}
    for sub in Subscriber.query.all():
        source = sub.source or 'direct'
        sources[source] = sources.get(source, 0) + 1

    # Calculate percentages
    for source, count in sources.items():
        percentage = round((count / total_count) * 100) if total_count > 0 else 0
        stats.append({
            'name': source,
            'count': count,
            'percentage': percentage
        })

    # Sort stats by count descending
    stats = sorted(stats, key=lambda x: x['count'], reverse=True)

    return render_template(
        'admin_dashboard.html',
        subscribers=subscribers,
        total_count=total_count,
        stats=stats,
        pagination=pagination,
        search_query=search_query
    )

@app.route('/admin/export_csv')
def export_csv():
    """Export subscriber data as a CSV file"""
    # Query all subscribers
    subscribers = Subscriber.query.order_by(Subscriber.created_at.asc()).all()

    # Create a CSV response
    def generate():
        # Write the header row
        yield ','.join(['ID', 'Name', 'Email', 'Source', 'Newsletter', 'Created At', 'Referral Code']) + '\n'
        # Write subscriber data rows
        for subscriber in subscribers:
            yield ','.join([
                str(subscriber.id),
                subscriber.name,
                subscriber.email,
                subscriber.source or 'Direct',
                'Yes' if subscriber.newsletter else 'No',
                subscriber.created_at.strftime('%Y-%m-%d %H:%M:%S') if subscriber.created_at else 'N/A',
                subscriber.referral_code or 'N/A'
            ]) + '\n'

    # Return the response with the appropriate headers
    return Response(
        generate(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=subscribers.csv'
        }
    )
