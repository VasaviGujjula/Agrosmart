from flask import Blueprint, render_template, request, jsonify, current_app
from groq import Groq

# Blueprint is registered in app.py with url_prefix='/api/chat'
chatbot_bp = Blueprint('chatbot', __name__)

# Language mapping for the AI
LANGUAGE_MAP = {
    "en-IN": "English",
    "hi-IN": "Hindi",
    "te-IN": "Telugu"
}

@chatbot_bp.route('/ask')
def sahayak_page():
    # This renders the full-page chat.html interface
    return render_template('chatbot/chat.html')

@chatbot_bp.route('/ask', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    lang_code = data.get('lang', 'en-IN')
    user_language = LANGUAGE_MAP.get(lang_code, "English")

    # Pulls your key from config.py
    api_key = current_app.config.get('GROQ_API_KEY')

    if not api_key:
        return jsonify({'response': "API Key missing in config.py"}), 500

    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are AgroSmart Sahayak, a farming assistant. "
                        f"Reply ONLY in {user_language}. "
                        f"Explain insurance and farming in very simple terms for farmers. "
                        f"Give step-by-step answers. "
                        f"IMPORTANT: Do NOT use markdown like **bold** or ## headers. Use plain text only."
                    )
                },
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5, # Lower temperature for more consistent, simple answers
        )

        # Extract the content
        ai_response = chat_completion.choices[0].message.content
        
        # Double clean the response to remove any accidental markdown
        clean_response = ai_response.replace("**", "").replace("#", "").strip()

        return jsonify({
            'response': clean_response,
            'reply': clean_response # Providing both keys for frontend compatibility
        })

    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return jsonify({'response': "I am resting for a moment. Please try again in 1 minute."}), 500