from database.db import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to access user details if needed
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))

    def __repr__(self):
        return f'<Notification {self.message[:20]}...>'