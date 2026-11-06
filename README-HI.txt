SHIVANKVERSE AI NEWS AGENT — FINAL STARTER PACKAGE

GITHUB UPLOAD STRUCTURE:
- app.py
- requirements.txt
- Procfile
- .gitignore
- .env.example
- README-HI.txt
- templates/index.html
- static/style.css
- static/app.js

IMPORTANT: templates and static are FOLDERS. Keep this exact structure.

RENDER DEPLOY:
Build command: pip install -r requirements.txt
Start command: gunicorn app:app

This is a starter web app:
- Loads technology headlines from RSS feeds.
- Lets you select a story and prepare a draft.
- Can call an OpenAI-compatible API if you configure an API key.
- Exports article HTML.

Limitations:
- RSS headlines are not fact-checked or trend-ranked.
- Without an API key it produces only a starter template, not a researched AI article.
- Blogger auto-publishing is not implemented yet.
- Add login/security and proper persistent storage before public production use.
- Never commit your .env or API key to GitHub.

Ownership: You receive the editable project source code and can modify and deploy it under your own accounts. Domain, hosting, API usage, and third-party account permissions remain under your control.
