from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('farmer', 'buyer', name='user_roles'), nullable=False)
        
    # --- NEW FIELDS ADDED HERE ---
    upi_id = db.Column(db.String(100), nullable=True) # For Payments
    district = db.Column(db.String(100), nullable=True) # For Mandi Filtering
    state = db.Column(db.String(100), nullable=True) # For Mandi Filtering
    # -----------------------------

    contracts_as_buyer = db.relationship('Contract', foreign_keys='Contract.buyer_id', backref='buyer', lazy=True)
    contracts_as_farmer = db.relationship('Contract', foreign_keys='Contract.farmer_id', backref='farmer', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)