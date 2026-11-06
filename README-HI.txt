SHIVANKVERSE AI NEWS AGENT — YOUR STARTER PROJECT

यह तुम्हारे लिए बनाया गया शुरुआती, editable web-app source code है।
इसे चलाने के लिए:
1. Windows laptop में Python 3.10+ install करो: https://www.python.org/downloads/
   Install करते समय "Add Python to PATH" चुनना।
2. ZIP extract करो।
3. START-WINDOWS.bat पर double-click करो।
4. Browser में http://127.0.0.1:5000 खोलो।

अभी क्या काम करता है:
- Global tech RSS feeds से headlines लाता है।
- Headline चुनकर source link editor में भरता है।
- AI API key न होने पर केवल सुरक्षित starter template देता है।
- API key configure होने पर compatible AI endpoint से Hindi draft बनाता है।
- Article को HTML file में export करता है।

AI चालू करने के लिए:
- .env.example की copy बनाकर उसका नाम .env रखो।
- OPENAI_API_KEY में अपनी API key भरो।
- AI_MODEL अपने provider के supported model से मिलाओ।
- API usage पर provider charges लग सकते हैं। API key किसी से share मत करना।

महत्वपूर्ण सीमाएँ:
- RSS feed trend-ranking या fact-checking नहीं है।
- यह अभी Blogger पर publish नहीं करता।
- अभी user review और source verification जरूरी है।
- इसे public internet पर deploy करने से पहले login/security जोड़ना जरूरी है।

OWNERSHIP:
इस package का source code तुम्हारे पास है। तुम इसे modify कर सकते हो, अपने नाम/brand से आगे develop कर सकते हो और अपने hosting/account पर deploy कर सकते हो। Domain, hosting, API keys और Blogger permissions तुम्हारे अपने accounts में होने चाहिए। यह package अपने-आप legal trademark, domain या third-party API rights transfer नहीं करता।

LIVE DEPLOY (Render):
1. GitHub.com par account banao aur New repository se private repo banao.
2. ZIP extract karke project ke saare files repo mein upload/commit karo.
3. Render.com par sign up/login karo; GitHub connect karo.
4. New > Web Service > apni repository select karo.
5. Build Command: pip install -r requirements.txt
6. Start Command: gunicorn app:app
7. Free instance choose karke Deploy karo.
8. Deploy successful hone par Render tumhe https://....onrender.com URL dega.

Note: Free service 15 min inactivity ke baad sleep ho sakti hai aur next open par start hone mein lagbhag 1 minute lag sakta hai. Local filesystem permanent storage nahi hai. Production use ke liye paid hosting + database/security recommended.
Official guide: https://render.com/docs/deploy-flask
