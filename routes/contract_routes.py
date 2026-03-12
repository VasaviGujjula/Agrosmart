from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.db import db
from models.contract_model import Contract
from utils.decorators import login_required, role_required
from utils.audit_helper import log_activity  # Added import
from datetime import datetime

contract_bp = Blueprint('contracts', __name__)

@contract_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('buyer')
def create():
    if request.method == 'POST':
        try:
            new_contract = Contract(
                buyer_id=session['user_id'],
                crop_type=request.form.get('crop_type'),
                quantity_quintals=float(request.form.get('quantity')),
                price_per_quintal=float(request.form.get('price')),
                quality_specifications=request.form.get('specs'),
                delivery_date=datetime.strptime(request.form.get('delivery_date'), '%Y-%m-%d'),
                status='open'
            )
            db.session.add(new_contract)
            db.session.commit()

            # --- Audit Log for Creation ---
            log_activity(
                action="CONTRACT_CREATED",
                table_name="contracts",
                record_id=new_contract.id
            )

            flash("Contract offer published successfully!", "success")
            return redirect(url_for('buyer.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash("Error creating contract. Please check your inputs.", "danger")
    
    return render_template('buyer/create_contract.html')

@contract_bp.route('/accept/<int:contract_id>', methods=['POST'])
@login_required
@role_required('farmer')
def accept_contract(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    
    # Validation: Ensure contract is still available
    if contract.status != 'open':
        flash("This contract is no longer available.", "warning")
        return redirect(url_for('farmer.dashboard'))

    try:
        # Update Contract State
        contract.farmer_id = session['user_id']
        contract.status = 'signed'
        contract.signed_at = datetime.utcnow()
        
        db.session.commit()

        # --- Audit Log for Acceptance ---
        log_activity(
            action="CONTRACT_ACCEPTED",
            table_name="contracts",
            record_id=contract_id
        )

        flash("Contract signed! You are now legally bound to this agreement.", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred during signing. Please try again.", "danger")
        
    return redirect(url_for('farmer.dashboard'))

@contract_bp.route('/view')
@login_required
def view_contracts():
    # Only show 'open' contracts that haven't been accepted yet
    all_contracts = Contract.query.filter_by(status='open').all()
    
    # We pass the list 'all_contracts' to the HTML template as the variable 'contracts'
    return render_template('contracts/view.html', contracts=all_contracts)

@contract_bp.route('/review-contract/<int:contract_id>')
@login_required
@role_required('farmer')
def review_contract(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    
    # Check if the contract is still available
    if contract.status.lower() not in ['open', 'pending']:
        flash("This contract is no longer available for signing.", "warning")
        return redirect(url_for('farmer.dashboard'))
        
    return render_template('farmer/review_contract.html', contract=contract)

##order status##
# In routes/contract_routes.py
@contract_bp.route('/update_status/<int:id>/<string:new_status>', methods=['POST'])
@login_required
def update_status(id, new_status):
    # ... (your existing imports)
    contract = Contract.query.get_or_404(id)
    
    valid_statuses = ['Pending', 'Paid', 'Shipped', 'Delivered', 'Cancelled']
    
    if new_status in valid_statuses:
        contract.status = new_status  # Updates the Dashboard badge
        
        # --- ADD THIS SYNC LOGIC ---
        if new_status in ['Shipped', 'Delivered']:
            contract.logistics_status = new_status # Updates the Tracking icons
        # ---------------------------
        
        db.session.commit()
        flash(f"Status updated to {new_status}!", "success")
    else:
        flash("Invalid status update.", "danger")
        
    return redirect(request.referrer or url_for('buyer.dashboard'))