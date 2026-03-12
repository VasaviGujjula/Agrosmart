def process_message(user_text, lang='en'):
    text = user_text.lower()
    
    # Simple Rule Engine
    knowledge_base = {
        'en': {
            'contract': 'Contracts are legally binding agreements between farmers and buyers.',
            'payment': 'Payments are released directly to your bank account after delivery.',
            'insurance': 'Crop insurance covers natural disasters like floods or droughts.'
        },
        'te': {
            'contract': 'కాంట్రాక్టులు రైతులకు మరియు కొనుగోలుదారులకు మధ్య చట్టబద్ధమైన ఒప్పందాలు.',
            'payment': 'డెలివరీ తర్వాత పేమెంట్లు నేరుగా మీ బ్యాంక్ ఖాతాకు పంపబడతాయి.',
            'insurance': 'వరదలు లేదా కరువు వంటి ప్రకృతి వైపరీత్యాల నుండి పంట భీమా రక్షణ కల్పిస్తుంది.'
        }
    }
    
    # Default fallback
    response = "I'm still learning. Try asking about 'contracts' or 'payments'."
    
    # Check for keywords
    for key, val in knowledge_base.get(lang, knowledge_base['en']).items():
        if key in text:
            response = val
            break
            
    return response