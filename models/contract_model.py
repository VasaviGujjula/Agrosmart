from database.db import db
from datetime import datetime

class Contract(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Shop & Personal Details
    shop_name = db.Column(db.String(200)) 
    buyer_mobile = db.Column(db.String(20))
    location = db.Column(db.String(200))
    quality_terms = db.Column(db.Text) 
    
    # Crop & Financial Details
    crop_type = db.Column(db.String(100), nullable=False)
    quantity_quintals = db.Column(db.Float, nullable=False)
    price_per_quintal = db.Column(db.Float, nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    
    # --- The Status Field ---
    # We use your previous default 'Awaiting Downpayment' as it's more professional
    status = db.Column(db.String(50), default='Awaiting Downpayment', nullable=False)

    transaction_id = db.Column(db.String(100), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Digital Signature field
    farmer_signature = db.Column(db.Text, nullable=True)

    # --- Crop Quality AI Verification Fields ---
    crop_image = db.Column(db.String(255), nullable=True)     # Path to image
    quality_score = db.Column(db.String(100), nullable=True)  # AI Result
    ai_status = db.Column(db.String(50), default="Pending")   # AI Status

    # --- Logistics & Tracking Fields ---
    tracking_id = db.Column(db.String(100), nullable=True)
    logistics_status = db.Column(db.String(50), default="Pending Shipment")

    def __repr__(self):
        return f'<Contract {self.crop_type} - {self.status}>'