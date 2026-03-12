import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Only run logging setup in the main process to avoid WinError 32 on Windows
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        # File Handler: Stores detailed logs for debugging
        file_handler = RotatingFileHandler('logs/agrosmart.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('AgroSmart Startup')