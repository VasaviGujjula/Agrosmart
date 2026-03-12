from flask import request, session
from database.db import db
from models.audit_model import AuditLog # You'll need to create this model

def log_activity(action, table_name=None, record_id=None):
    user_id = session.get('user_id')
    new_log = AuditLog(
        user_id=user_id,
        action=action,
        table_name=table_name,
        record_id=record_id,
        ip_address=request.remote_addr
    )
    db.session.add(new_log)
    db.session.commit()