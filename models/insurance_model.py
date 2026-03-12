from database.db import db
from datetime import datetime

class InsurancePolicy(db.Model):
    __tablename__ = 'insurance_policies'
    
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=False)
    policy_number = db.Column(db.String(50), unique=True, nullable=False)
    premium_amount = db.Column(db.Numeric(10, 2), nullable=False)
    coverage_amount = db.Column(db.Numeric(12, 2), nullable=False)
    # ADDED NAME: 'policy_status'
    status = db.Column(db.Enum('Applied', 'Active', 'Pending', 'Claimed', 'Expired', name='policy_status'), default='Applied')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class InsuranceClaim(db.Model):
    __tablename__ = 'insurance_claims'
    
    id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('insurance_policies.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    proof_link = db.Column(db.String(255)) # URL to image/report
    amount_requested = db.Column(db.Numeric(12, 2), nullable=False)
    # Status: 'pending', 'approved', 'rejected'
    # ADDED NAME: 'claim_status'
    status = db.Column(db.Enum('Pending', 'Claimed', 'Approved', 'Rejected', name='claim_status'), default='Pending')
    admin_remarks = db.Column(db.Text)
    filed_at = db.Column(db.DateTime, default=datetime.utcnow)