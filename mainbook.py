from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import google.generativeai as genai
import re

app = Flask(__name__)

# Configure Gemini 1.5 Flash
genai.configure(api_key="AIzaSyAcTqz4eSXuE-rPzeQ06UGPPfgPV_tsq4A")  # Replace with your actual API key
model = genai.GenerativeModel('gemini-1.5-flash')

# CORS Setup
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
    return response

def clean_text(text):
    """Remove citations and clean whitespace"""
    return re.sub(r'\[\d+\]', '', text).strip()

def fetch_book_data(book_title, author):
    """Multi-source scraper optimized for plot extraction"""
    sources = {
        "Wikipedia": f"https://en.wikipedia.org/wiki/{quote(book_title.replace(' ', '_'))}",
        "Goodreads": f"https://www.goodreads.com/search?q={quote(book_title)}+{quote(author)}",
        "Google Books": f"https://www.googleapis.com/books/v1/volumes?q=intitle:{quote(book_title)}+inauthor:{quote(author)}"
    }
    
    collected_data = []
    
    # Wikipedia Scraper
    try:
        wiki_res = requests.get(sources["Wikipedia"], headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        if wiki_res.status_code == 200:
            soup = BeautifulSoup(wiki_res.text, 'html.parser')
            plot_sections = ['Plot', 'Summary', 'Synopsis']
            for section in plot_sections:
                span = soup.find('span', {'id': section})
                if span:
                    content = []
                    for elem in span.parent.find_next_siblings(['p', 'h2']):
                        if elem.name == 'h2':
                            break
                        content.append(clean_text(elem.get_text()))
                    if content:
                        collected_data.append(f"Wikipedia {section}:\n" + "\n".join(content[:3]))
                        break
    except:
        pass
    
    # Goodreads Fallback
    try:
        gr_res = requests.get(sources["Goodreads"], headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        if gr_res.status_code == 200:
            soup = BeautifulSoup(gr_res.text, 'html.parser')
            desc = soup.find('div', {'id': 'description'})
            if desc:
                collected_data.append("Goodreads Description:\n" + clean_text(desc.find_all('span')[-1].get_text()))
    except:
        pass
    
    # Google Books Fallback
    try:
        gb_res = requests.get(sources["Google Books"], timeout=5)
        if gb_res.status_code == 200:
            data = gb_res.json()
            if data.get('items'):
                desc = data['items'][0]['volumeInfo'].get('description')
                if desc:
                    collected_data.append("Google Books Description:\n" + clean_text(desc))
    except:
        pass
    
    return "\n\n".join(collected_data) if collected_data else None

@app.route('/api/summarize', methods=['POST', 'OPTIONS'])
def summarize():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        book_title = data.get('bookTitle', '').strip()
        author = data.get('author', '').strip()

        if not book_title:
            return jsonify({'error': 'Book title is required'}), 400

        # Step 1: Fetch raw data
        raw_data = fetch_book_data(book_title, author)
        if not raw_data:
            return jsonify({'error': 'No book data found'}), 404

        # Step 2: Generate summary with Gemini 1.5 Flash
        prompt = f"""
        Generate a comprehensive 6-8 paragraph book summary with these points:

1. Introduction: (1 paragraph):
   - Book title and author context
   - Main theme or premise

2. Plot Summary: (3-4 paragraphs):
   - Detailed chronological plot progression
   - Key events with explanations
   - Main character arcs

3. Analysis: (2 paragraphs):
   - Major themes and symbols
   - Author's message or social commentary
   - Notable literary techniques

4. Conclusion: (1 paragraph):
   - Overall impact/legacy
   - Why it remains relevant

Write in clear, engaging prose at a college reading level. 
Include specific examples and quotations where available.
Write naturally book tittle and author name without highlighting the title.
        
        Source data:
        {raw_data}
        """
        
        response = model.generate_content(prompt)
        summary = response.text

        return jsonify({
            'summary': summary,
            'model': 'gemini-1.5-flash'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)