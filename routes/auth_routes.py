from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user_model import User
from database.db import db

# Define the blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 1. Extract Data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        phone = request.form.get('phone')
        # --- NEW: Get UPI ID from form ---
        upi_id = request.form.get('upi_id')

        # 2. Validation
        if not username or not email or not password or not role or not phone:
            flash("All fields are required.", "danger")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash("Email already exists. Please login.", "warning")
            return redirect(url_for('auth.login'))

        # 3. Create and Save User
        try:
            # Create the object with upi_id included
            new_user = User(
                username=username, 
                email=email, 
                phone=phone, 
                role=role,
                upi_id=upi_id  # --- NEW: Save UPI ID to database ---
            )
            new_user.set_password(password) # This hashes the password
            
            db.session.add(new_user)
            db.session.commit()
            
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            # Log the error to your terminal so you can see what went wrong
            print(f"Registration Error: {e}")
            flash("An error occurred during registration. Please try again.", "danger")
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Establish Session
            session.permanent = True 
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            flash(f"Welcome back, {user.username}!", "success")
            
            # Dynamic redirection based on role
            return redirect(url_for(f'{user.role}.dashboard'))
        
        flash("Invalid email or password.", "danger")
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))