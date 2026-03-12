from database.db import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    # ADDED NAME: 'payment_status'
    status = db.Column(db.Enum('pending', 'completed', 'failed', name='payment_status'), default='pending')
    payment_method = db.Column(db.String(50))
    transaction_reference = db.Column(db.String(100), unique=True)
    paid_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))
    # ADDED NAME: 'transaction_type'
    type = db.Column(db.Enum('credit', 'debit', name='transaction_type'), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)