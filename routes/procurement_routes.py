from flask import Blueprint, render_template
from models import User, db

# Create the Blueprint
procurement_bp = Blueprint('procurement', __name__)

# routes/procurement_routes.py
@procurement_bp.route('/procurement_dashboard')
def procurement_dashboard():
    # This fetches all users where the role is 'farmer' (case-insensitive)
    all_farmers = User.query.filter(User.role.ilike('farmer')).all()
    return render_template('buyer/dashboard.html', farmers=all_farmers)