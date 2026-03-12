from database.db import db

class FarmerProfile(db.Model):
    __tablename__ = 'farmer_profiles'
    
    # This must match the column we just added in SQL
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    full_name = db.Column(db.String(100))
    location = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    land_size_acres = db.Column(db.Float)
    crop_types = db.Column(db.String(255))
    bank_account_no = db.Column(db.String(20))
    ifsc_code = db.Column(db.String(20))
    insurance_eligible = db.Column(db.Boolean, default=True)

    # This allows you to call user.farmer_profile
    user = db.relationship('User', backref=db.backref('farmer_profile', uselist=False))

    def __repr__(self):
        return f'<FarmerProfile for {self.full_name}>'