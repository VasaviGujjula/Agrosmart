from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from database.db import db
from models.user_model import User
from models.buyer_model import BuyerProfile
from models.contract_model import Contract 
from models.payment_model import Payment    
from utils.decorators import login_required, role_required

buyer_bp = Blueprint('buyer', __name__)

# --- BUYER DASHBOARD ---
@buyer_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session.get('user_id')
    contracts = Contract.query.filter_by(buyer_id=user_id).all()
    farmers = User.query.filter_by(role='farmer').all()
    total_posted = len(contracts)
    active_farmers_count = len(farmers)
    
    return render_template(
        'buyer/dashboard.html', 
        contracts=contracts, 
        farmers=farmers, 
        total_posted=total_posted, 
        active_farmers=active_farmers_count
    )

# --- BUYER PROFILE MANAGEMENT ---
@buyer_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('buyer')
def profile():
    user_id = session.get('user_id')
    profile = BuyerProfile.query.filter_by(buyer_id=user_id).first()

    if request.method == 'POST':
        if not profile:
            profile = BuyerProfile(buyer_id=user_id)
            db.session.add(profile)

        profile.company_name = request.form.get('company_name')
        profile.registration_no = request.form.get('registration_no')
        profile.contact_person = request.form.get('contact_person')
        profile.delivery_address = request.form.get('delivery_address')
        profile.required_crops = request.form.get('required_crops')
        profile.quality_standards = request.form.get('quality_standards')
        profile.contract_preference = request.form.get('contract_preference')

        db.session.commit()
        flash("Company profile updated successfully.", "success")
        return redirect(url_for('buyer.profile'))

    return render_template('buyer/profile.html', profile=profile)

# --- CREATING CONTRACT WITH WHATSAPP NOTIFICATION ---
@buyer_bp.route('/create-contract', methods=['GET', 'POST'])
@login_required
def create():
    selected_farmer = None
    farmer_id_arg = request.args.get('farmer_id')
    
    if farmer_id_arg:
        selected_farmer = User.query.get(farmer_id_arg)

    if request.method == 'POST':
        f_id = request.form.get('farmer_id')
        if f_id:
            selected_farmer = User.query.get(f_id)

        new_contract = Contract(
            buyer_id=session.get('user_id'),
            farmer_id=f_id,
            shop_name=request.form.get('shop_name'),
            buyer_mobile=request.form.get('buyer_mobile'),
            crop_type=request.form.get('crop_type'),
            quantity_quintals=request.form.get('quantity_quintals'),
            price_per_quintal=request.form.get('price_per_quintal'),
            delivery_date=request.form.get('delivery_date'),
            location=request.form.get('location'),
            quality_terms=request.form.get('quality_terms'),
            status='Awaiting Downpayment'
        )

        try:
            db.session.add(new_contract)
            db.session.commit()

            if selected_farmer and selected_farmer.phone:
                import urllib.parse
                message = f"Namaste {selected_farmer.username}, I have created a contract for {new_contract.crop_type} on Agrosmart. Please review it!"
                safe_msg = urllib.parse.quote(message)
                whatsapp_url = f"https://wa.me/{selected_farmer.phone}?text={safe_msg}"
                
                return render_template('buyer/redirect_whatsapp.html', 
                                       url=whatsapp_url, 
                                       contract_id=new_contract.id,
                                       farmer_name=selected_farmer.username)

            return redirect(url_for('buyer.payment_page', contract_id=new_contract.id))

        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('buyer.dashboard'))

    return render_template('buyer/create_contract.html', farmer=selected_farmer)

# --- PAYMENTS ---#
# buyer_routes.py
@buyer_bp.route('/payment/<int:contract_id>')
@login_required
def payment_page(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    
    # 1. Get the Farmer who is part of this contract
    # Assuming Mani is the farmer_id in this contract
    farmer = User.query.get(contract.farmer_id) 
    
    # 2. Get Mani's UPI ID from his profile
    # Ensure your User model has a 'upi_id' column
    upi_to_pay = farmer.upi_id if farmer.upi_id else "default@upi"

    # 3. Calculate total amount
    total_amount = contract.quantity_quintals * contract.price_per_quintal

    return render_template('buyer/payment.html', 
                           contract=contract, 
                           amount=total_amount, 
                           upi_id=upi_to_pay) # This sends Mani's UPI to the QR code

##---process payment---##
@buyer_bp.route('/process-payment/<int:contract_id>', methods=['POST'])
@login_required
def process_payment(contract_id):
    # 1. Fetch the contract being paid for
    contract = Contract.query.get_or_404(contract_id)
    
    # 2. Get the real Razorpay Transaction ID from the hidden form
    transaction_id = request.form.get('transaction_id')

    if not transaction_id:
        flash("Payment verification failed. No transaction ID received.", "warning")
        return redirect(url_for('buyer.payment_page', contract_id=contract.id))

    try:
        # 3. Update the contract details
        contract.status = 'Paid (Awaiting Farmer Signature)'
        contract.transaction_id = transaction_id # Stores the rzp_test_... ID
        
        # 4. Save to database
        db.session.commit()
        
        # 5. Send the buyer to your beautiful success page
        return redirect(url_for('buyer.payment_success', contract_id=contract.id))

    except Exception as e:
        # If database crashes, undo changes so data isn't corrupted
        db.session.rollback()
        print(f"Database Error: {e}") # Helpful for your debugging
        flash("Payment received but status update failed. Please notify the farmer.", "danger")
        return redirect(url_for('buyer.dashboard'))

@buyer_bp.route('/payment-success/<int:contract_id>')
@login_required
def payment_success(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    # Renders your payment_success.html template
    return render_template('buyer/payment_success.html', contract=contract)

#---Receipt Downloading---#
import io
from flask import send_file
from fpdf import FPDF

@buyer_bp.route('/download_receipt/<int:contract_id>')
@login_required
def download_receipt(contract_id):
    try:
        contract = Contract.query.get_or_404(contract_id)
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", 'B', 16)
        pdf.cell(190, 10, "AGROSMART DIGITAL RECEIPT", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("helvetica", size=12)
        pdf.cell(100, 10, f"Contract ID: #{contract.id}")
        pdf.cell(90, 10, f"Date: {contract.delivery_date}", ln=True, align='R')
        pdf.line(10, 40, 200, 40)
        pdf.ln(10)

        pdf.cell(190, 10, f"Buyer/Shop: {contract.shop_name}", ln=True)
        pdf.cell(190, 10, f"Crop: {contract.crop_type}", ln=True)
        pdf.cell(190, 10, f"Quantity: {contract.quantity_quintals} Qtl", ln=True)
        pdf.cell(190, 10, f"Price: Rs. {contract.price_per_quintal}/Qtl", ln=True)
        
        pdf.ln(5)
        pdf.set_font("helvetica", 'B', 14)
        total = float(contract.quantity_quintals or 0) * float(contract.price_per_quintal or 0)
        pdf.cell(190, 10, f"Total Amount Paid: Rs. {total}", ln=True)
        
        pdf_bytes = pdf.output() 
        buffer = io.BytesIO(pdf_bytes)
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"Receipt_{contract.id}.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        print(f"CRITICAL PDF ERROR: {e}")
        flash("Could not generate receipt.", "danger")
        return redirect(url_for('buyer.dashboard'))
    

##---track_order---##
@buyer_bp.route('/track/<int:contract_id>')
def track_order(contract_id):
    from models.contract_model import Contract
    contract = Contract.query.get_or_404(contract_id)
    return render_template('buyer/track_order.html', contract=contract)

##---securing---##
@buyer_bp.route('/submit_payment/<int:contract_id>', methods=['POST'])
@login_required
def submit_payment(contract_id):
    utr_number = request.form.get('utr_number')
    contract = Contract.query.get_or_404(contract_id)

    # 1. Check if the UTR is empty or too short (Basic Validation)
    if not utr_number or len(utr_number) < 12:
        flash("Invalid UTR! Please enter the 12-digit transaction ID from your bank receipt.", "danger")
        return redirect(url_for('buyer.payment_page', contract_id=contract_id))

    # 2. Mock Verification (In a real app, you'd call a Bank API here)
    if utr_number == "000000000000": # Example of a blocked "fake" UTR
        flash("Payment Verification Failed: UTR not found in banking records.", "danger")
        return redirect(url_for('buyer.payment_page', contract_id=contract_id))

    # 3. Only update if validation passes
    contract.utr_id = utr_number
    contract.status = 'Paid' # Or 'Payment Under Verification'
    db.session.commit()
    
    flash("Payment submitted successfully! The farmer will verify this shortly.", "success")
    return redirect(url_for('buyer.dashboard'))