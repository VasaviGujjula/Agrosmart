from app import create_app
from database.db import db
# This manually forces Python to read the models in the right order
from models.user_model import User
from models.contract_model import Contract
from models.payment_model import Payment
from models.farmer_model import FarmerProfile
from models.buyer_model import BuyerProfile
from models.insurance_model import InsurancePolicy

app = create_app()
with app.app_context():
    print("Deleting old database...")
    db.drop_all()
    print("Creating new database with correct relations...")
    db.create_all()
    print("✅ Success! Your local database is ready.")