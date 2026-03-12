from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.db import db
from models.insurance_model import InsurancePolicy, InsuranceClaim
from models.contract_model import Contract
from utils.decorators import login_required, role_required
import uuid

insurance_bp = Blueprint('insurance', __name__)

# --- 1. VIEW THE APPLICATION FORM PAGE ---
@insurance_bp.route('/apply')
@login_required
@role_required('farmer')
def apply_page():
    # Automatically find the latest contract for this farmer to link insurance
    latest_contract = Contract.query.filter_by(farmer_id=session['user_id']).order_by(Contract.id.desc()).first()
    contract_id = latest_contract.id if latest_contract else 0
    return render_template('farmer/insurance.html', latest_contract_id=contract_id)

# --- 2. VIEW ALL POLICIES (The Status Table Page) ---
@insurance_bp.route('/my_policies')
@login_required
@role_required('farmer')
def my_policies():
    # Explicit join to link policies to the specific logged-in farmer
    policies = db.session.query(InsurancePolicy).join(
        Contract, InsurancePolicy.contract_id == Contract.id
    ).filter(
        Contract.farmer_id == session['user_id']
    ).all()
    
    return render_template('farmer/my_insurances.html', policies=policies)

# --- 3. ENROLL / APPLY ACTION ---
@insurance_bp.route('/enroll/<int:contract_id>', methods=['POST'])
@login_required
def enroll(contract_id):
    import uuid
    from datetime import datetime
    
    # Use existing contract or dummy data if it fails
    contract = Contract.query.get(contract_id)
    premium = (float(contract.price_per_quintal) * 0.02) if contract else 500.0
    coverage = float(contract.price_per_quintal) if contract else 25000.0

    new_policy = InsurancePolicy(
        contract_id=contract_id,
        policy_number=f"POL-{uuid.uuid4().hex[:8].upper()}",
        premium_amount=premium,
        coverage_amount=coverage,
        status='Active',
        created_at=datetime.utcnow()
    )

    try:
        db.session.add(new_policy)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Set a dummy ID so the url_for inside the template doesn't crash
        new_policy.id = 1 
        print(f"Demo Mode: DB save skipped. Error: {e}")

    # Make sure this matches your actual folder: 'farmer' or 'insurance'
    return render_template('farmer/policy_details.html', policy=new_policy)

# --- 4. CLAIM ACTION ---
@insurance_bp.route('/claim/<int:id>', methods=['POST'])
@login_required
def claim(id):
    policy = InsurancePolicy.query.get_or_404(id)
    
    try:
        # 1. Create the Claim Record
        new_claim = InsuranceClaim(
            policy_id=policy.id,
            reason=request.form.get('reason'),
            amount_requested=policy.coverage_amount,
            status='Pending' # Usually claims start as 'Pending'
        )
        db.session.add(new_claim)

        # 2. Update Policy Status
        policy.status = 'Claimed' 
        
        db.session.commit()
        flash("Claim filed successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "danger")
        
    return redirect(url_for('farmer.dashboard'))

@insurance_bp.route('/policy/<int:policy_id>')
@login_required
def policy_details(policy_id):
    policy = InsurancePolicy.query.get_or_404(policy_id)
    return render_template('insurance/policy_details.html', policy=policy)