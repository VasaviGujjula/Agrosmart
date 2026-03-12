from database.db import db

class BuyerProfile(db.Model):
    __tablename__ = 'buyer_profiles'
    
    # FIX: Changed 'users.id' to 'user.id' to match your User model __tablename__
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    
    company_name = db.Column(db.String(150), nullable=False)
    registration_no = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)
    
    # Procurement Preferences
    required_crops = db.Column(db.Text, nullable=True)  # List of crops they usually buy
    quality_standards = db.Column(db.Text, nullable=True) # e.g., "Grade A only", "Moisture < 12%"
    
    # Fixed Enum implementation
    contract_preference = db.Column(db.String(50), default='fixed_price') 

    # Relationship back to User
    user = db.relationship('User', backref=db.backref('buyer_profile', uselist=False))

    def __repr__(self):
        return f'<BuyerProfile for {self.company_name}>'