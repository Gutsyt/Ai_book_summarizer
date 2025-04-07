# Ai_book_summarizer 
# AI-Powered Book Summarizer
https://github.com/yourusername/book-summarizer

_A Flask web application that generates book summaries using Gemini 1.5 Flash API and web scraping._

## Features
- Multi-Source Scraping: Fetches data from Wikipedia, Goodreads, and Google Books
- AI-Powered Summaries: Uses Gemini 1.5 Flash for 800-1000 word summaries
- Clean Formatting: Paragraph-style output without section headings
- Responsive UI: Works on desktop and mobile devices
- Free Access: No subscriptions or payments required

## Technologies Used
- Backend: Python, Flask, Gemini API
- Frontend: HTML5, CSS3, JavaScript
- Scraping: BeautifulSoup, Requests
- APIs: Google Books API

## Installation
1. Clone the repository:
git clone https://github.com/yourusername/book-summarizer.git
cd book-summarizer

2. Install dependencies:
pip install flask requests beautifulsoup4 google-generativeai python-dotenv

3. Set up your Gemini API key:
  setup your own api key in mainbook.py //line no. 11
  //genai.configure(api_key="enter your key")  # Replace with your actual API key


## Project Structure
book-summarizer/
├── app.py                # Flask backend
├── static/
│   ├── css/style.css     # Frontend styles
│   └── js/script.js      # Frontend logic
├── templates/
│   └── index.html        # Main page
├── .env                  # API keys (gitignored)
└── README.md             # This file


## Contributing
1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Challenges & Solutions
- **CORS Errors**: Implemented Flask-CORS middleware
- **Scraping Blocks**: Used rotating user-agents and delays
- **API Rate Limits**: Added fallback sources

## Future Scope
- User authentication
- Summary history saving
- Audiobook integration (Text-to-Speech)
- Genre-specific summarization

## License
Distributed under the MIT License. 


Project Link: https://github.com/yourusername/book-summarizer

