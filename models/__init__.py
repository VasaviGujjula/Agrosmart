# models/__init__.py
from database.db import db       # This connects to your database instance
from .user_model import User     # This exports the User class from user_model.py
from .contract_model import Contract
from .insurance_model import InsurancePolicy
from models.notification_model import Notification
from models.audit_model import AuditLog
# ... other models