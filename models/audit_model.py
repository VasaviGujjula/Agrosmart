from database.db import db
from datetime import datetime

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    
    # THIS IS THE MISSING PART: You must have a ForeignKey here
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    action = db.Column(db.String(255), nullable=False)
    target_table = db.Column(db.String(50))
    target_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship (This is what was failing because it couldn't find the FK above)
    user = db.relationship('User', backref='logs')

    def __repr__(self):
        return f'<AuditLog {self.action} by User {self.user_id}>'