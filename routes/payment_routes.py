from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from database.db import db
from models.payment_model import Payment, Transaction
from models.contract_model import Contract
from utils.decorators import login_required, role_required

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/farmer/dashboard')
@login_required
@role_required('farmer')
def farmer_payments():
    user_id = session.get('user_id')
    # Get all earnings
    transactions = Transaction.query.filter_by(
        user_id=user_id, 
        type='credit'
    ).order_by(Transaction.created_at.desc()).all()
    
    total_earned = sum(t.amount for t in transactions)
    return render_template('farmer/payments.html', transactions=transactions, total_earned=total_earned)


##----payment----## 
@payment_bp.route('/buyer/dashboard')
@login_required
@role_required('buyer')
def buyer_payments():
    user_id = session.get('user_id')
    # Get all payments made
    payments = Payment.query.filter_by(buyer_id=user_id).order_by(Payment.paid_at.desc()).all()
    total_spent = sum(p.amount for p in payments)
    return render_template('buyer/payments.html', payments=payments, total_spent=total_spent)


@payment_bp.route('/release/<int:contract_id>', methods=['POST'])
@login_required
@role_required('buyer')
def release_payment(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    
    if contract.buyer_id != session['user_id']:
        flash("Unauthorized.", "danger")
        return redirect(url_for('buyer.dashboard'))

    # Get the Transaction ID (UTR) from the payment form
    utr_no = request.form.get('transaction_id')
    
    if not utr_no:
        flash("UTR/Transaction ID is required to process payment.", "warning")
        return redirect(url_for('buyer.payment_page', contract_id=contract.id))

    amount = float(contract.quantity_quintals or 0) * float(contract.price_per_quintal or 0)
    
    # 1. Create Payment record with the UTR number
    pay = Payment(
        contract_id=contract.id,
        buyer_id=contract.buyer_id,
        farmer_id=contract.farmer_id,
        amount=amount,
        transaction_id=utr_no,  # Store the UTR entered by the buyer
        status='completed'      # You can set it to 'completed' since they've paid via UPI
    )
    db.session.add(pay)
    db.session.flush() 

    # 2. Create Ledger Entries (Transactions table)
    debit = Transaction(user_id=contract.buyer_id, payment_id=pay.id, type='debit', amount=amount, description=f"Paid for Contract #{contract.id} (UTR: {utr_no})")
    credit = Transaction(user_id=contract.farmer_id, payment_id=pay.id, type='credit', amount=amount, description=f"Earnings from Contract #{contract.id} (UTR: {utr_no})")
    
    # 3. Update Contract Status
    contract.status = 'completed'
    
    db.session.add_all([debit, credit])
    db.session.commit()
    
    flash(f"Payment of ₹{amount} recorded successfully!", "success")
    return redirect(url_for('payment.buyer_payments'))