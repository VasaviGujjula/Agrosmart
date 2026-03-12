from chatbot.language_handler import LanguageHandler

def process_message(message, lang_code='en'):
    msg = message.lower()
    
    # Intent mapping logic
    if any(word in msg for word in ['contract', 'agreement', 'ఒప్పందం', 'contract', 'अनुबंध']):
        intent = 'contract_info'
    elif any(word in msg for word in ['insurance', 'policy', 'భీమా', 'बीमा']):
        intent = 'insurance_info'
    elif any(word in msg for word in ['payment', 'money', 'డబ్బు', 'paisa', 'भुगतान']):
        intent = 'payment_info'
    elif any(word in msg for word in ['hi', 'hello', 'namaste', 'నమస్కారం']):
        intent = 'welcome'
    else:
        intent = 'fallback'

    return LanguageHandler.get_response(intent, lang_code)