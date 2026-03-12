class LanguageHandler:
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'te': 'Telugu',
        'hi': 'Hindi'
    }

    RESPONSES = {
        'en': {
            'welcome': "Hello! I am AgroSmart Sahayak. How can I help you today?",
            'contract_info': "Contracts are digital agreements between you and the buyer. Once signed, they are legally binding.",
            'insurance_info': "You can enroll in insurance for 2% of your contract value. Claims are processed within 7 days.",
            'payment_info': "Payments are released by the buyer once delivery is confirmed. You can check your earnings in the dashboard.",
            'fallback': "I'm sorry, I didn't understand that. Please ask about contracts, insurance, or payments."
        },
        'te': {
            'welcome': "నమస్కారం! నేను ఆగ్రోస్మార్ట్ సహాయక్. నేను మీకు ఎలా సహాయపడగలను?",
            'contract_info': "కాంట్రాక్టులు మీకు మరియు కొనుగోలుదారుకు మధ్య ఉన్న డిజిటల్ ఒప్పందాలు.",
            'insurance_info': "మీరు మీ కాంట్రాక్ట్ విలువలో 2% చెల్లించి భీమా పొందవచ్చు.",
            'payment_info': "డెలివరీ ధృవీకరించబడిన తర్వాత కొనుగోలుదారు ద్వారా పేమెంట్లు విడుదల చేయబడతాయి.",
            'fallback': "క్షమించండి, నాకు అర్థం కాలేదు. దయచేసి కాంట్రాక్టులు లేదా భీమా గురించి అడగండి."
        },
        'hi': {
            'welcome': "नमस्ते! मैं एग्रोस्मार्ट सहायक हूँ। मैं आपकी क्या मदद कर सकता हूँ?",
            'contract_info': "अनुबंध आपके और खरीदार के बीच डिजिटल समझौते हैं।",
            'insurance_info': "आप अपने अनुबंध मूल्य के 2% पर बीमा के लिए नामांकन कर सकते हैं।",
            'payment_info': "वितरण की पुष्टि होने के बाद खरीदार द्वारा भुगतान जारी किया जाता है।",
            'fallback': "क्षमा करें, मुझे समझ नहीं आया। कृपया अनुबंध या बीमा के बारे में पूछें।"
        }
    }

    @classmethod
    def get_response(cls, intent, lang_code):
        lang_data = cls.RESPONSES.get(lang_code, cls.RESPONSES['en'])
        return lang_data.get(intent, lang_data['fallback'])