import os
import requests  # Added missing import
import xml.etree.ElementTree as ET
from flask import Blueprint, render_template, current_app

market_bp = Blueprint('market', __name__)

@market_bp.route('/marketplace')
def marketplace():
    mandi_prices = []
    # Use the absolute path to ensure Python finds the files
    base_path = os.path.dirname(os.path.abspath(current_app.root_path))
    xml_files = ['data.xml', 'Data2.xml'] 
    
    for xml_filename in xml_files:
        # This force-checks the main project folder
        xml_path = os.path.join(current_app.root_path, xml_filename)

        try:
            if os.path.exists(xml_path):
                tree = ET.parse(xml_path)
                root = tree.getroot()
                
                # Government XML files often have a namespace or nested structure
                # Use './/record' to find tags regardless of depth
                for record in root.findall('.//record'): 
                    mandi_prices.append({
                        'state': record.findtext('state') or "N/A",
                        'market': record.findtext('market') or "N/A",
                        'commodity': record.findtext('commodity') or "N/A",
                        'modal_price': record.findtext('modal_price') or "0"
                    })
            else:
                print(f"DEBUG: File not found at {xml_path}")
        except Exception as e:
            print(f"DEBUG: Error parsing {xml_filename}: {e}")

    # ... keep your news logic here ...
    return render_template('farmer/marketplace.html', prices=mandi_prices, news=agri_news)

    # News Data Logic
    agri_news = []
    if news_key:
        try:
            news_api_url = f"https://newsapi.org/v2/everything?q=agriculture+india&apiKey={news_key}&pageSize=5"
            n_res = requests.get(news_api_url, timeout=5)
            if n_res.status_code == 200:
                articles = n_res.json().get('articles', [])
                agri_news = [{
                    'title': a['title'], 
                    'url': a['url'], 
                    'source': a['source']['name'], 
                    'published': a['publishedAt'][:10]
                } for a in articles]
        except Exception as e:
            print(f"DEBUG: News API Error: {e}")

    # Return render_template with all variables
    return render_template('farmer/marketplace.html', 
                           prices=mandi_prices, 
                           error=api_error, 
                           news=agri_news)