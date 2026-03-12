import os
from flask import Flask, render_template, redirect, url_for, session, request
from config import Config
from database.db import db, init_db
from utils.logger import setup_logging
from flask_migrate import Migrate

# --- 1. LANGUAGE DICTIONARY ---
LANGUAGES = {
    'en': {
        'hero_title': 'Connecting Farmers to the Future',
        'hero_subtitle': 'Smart contracts, AI guidance, and direct marketplace access.',
        'login': 'Login',
        'register': 'Register',
        'feature_1_title': 'AI Farming Assistant',
        'feature_1_desc': 'Get real-time crop advice and pest solutions in your pocket.',
        'feature_2_title': 'Smart Marketplace',
        'feature_2_desc': 'Secure contracts between farmers and buyers with no middlemen.',
        'feature_3_title': 'Crop Insurance',
        'feature_3_desc': 'Protect your harvest from unpredictable weather and risks.',
        'feature_4_title': 'Direct Payments',
        'feature_4_desc': 'Fast, secure, and transparent digital payments for your crops.'
    },
    'te': {
        'hero_title': 'రైతులకు భవిష్యత్తును కనెక్ట్ చేస్తోంది',
        'hero_subtitle': 'స్మార్ట్ కాంట్రాక్టులు, AI మార్గదర్శకత్వం మరియు నేరుగా మార్కెట్ యాక్సెస్.',
        'login': 'లాగిన్',
        'register': 'రిజిస్టర్'
    }
}

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- DATABASE CONFIGURATION ---
    database_url = os.environ.get('DATABASE_URL')

    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Logging
    if not os.path.exists('logs'):
        os.makedirs('logs')

    setup_logging(app)

    # Database init
    init_db(app)

    migrate = Migrate(app, db)

    # --- CREATE TABLES ---
    with app.app_context():
        try:
            from models.user_model import User
            from models.contract_model import Contract
            from models.payment_model import Payment
            from models.farmer_model import FarmerProfile
            from models.buyer_model import BuyerProfile
            from models.insurance_model import InsurancePolicy

            db.create_all()

            print("AgroSmart database initialized")

        except Exception as e:
            print("Database Error:", e)

    @app.context_processor
    def inject_lang():
        user_lang = session.get('lang', 'en')
        return {'lang_data': LANGUAGES.get(user_lang, LANGUAGES['en'])}

    @app.route('/set_language/<lang_code>')
    def set_language(lang_code):
        session['lang'] = lang_code
        return redirect(request.referrer or url_for('index'))

    # --- IMPORT BLUEPRINTS ---
    from routes.auth_routes import auth_bp
    from routes.contract_routes import contract_bp
    from routes.chatbot_routes import chatbot_bp
    from routes.farmer_routes import farmer_bp
    from routes.buyer_routes import buyer_bp
    from routes.insurance_routes import insurance_bp
    from routes.payment_routes import payment_bp
    from routes.marketplace_routes import market_bp
    from routes.procurement_routes import procurement_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(contract_bp, url_prefix='/contracts')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chat')
    app.register_blueprint(payment_bp, url_prefix='/payments')
    app.register_blueprint(insurance_bp, url_prefix='/insurance')
    app.register_blueprint(farmer_bp, url_prefix='/farmer')
    app.register_blueprint(buyer_bp, url_prefix='/buyer')
    app.register_blueprint(procurement_bp, url_prefix='/procurement')
    app.register_blueprint(market_bp, url_prefix='/market')

    @app.route('/')
    def index():
        if 'user_id' in session:
            try:
                return redirect(url_for(f"{session['role']}.dashboard"))
            except:
                return redirect(url_for('auth.login'))

        return render_template('index.html')

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)