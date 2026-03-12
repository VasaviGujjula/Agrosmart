import os

class Config:
    # 1. Security & Sessions
    # This combines your two secret key blocks into one clean line
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'agro-smart-secret-key-123'
    
    # 2. Database Configuration
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:vasu@localhost/agrosmart?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 3. AI Configuration (Groq)
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', 'paste_your_key_here_as_fallback')

    # 4. Mandi API Configuration
    # This tries to get the key from your computer first; if not found, it uses the sample key
    MANDI_API_KEY = os.environ.get('MANDI_API_KEY') or "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"

    # 5. News API Configuration
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY') or "c3a04b279b99488090f7129f367ad7fc"

    