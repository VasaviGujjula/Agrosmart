from flask_sqlalchemy import SQLAlchemy

# 1. Create the instance once here
db = SQLAlchemy()

def init_db(app):
    # 2. Bind it to the app
    # Only call this if it's not already initialized
    if "sqlalchemy" not in app.extensions:
        db.init_app(app)