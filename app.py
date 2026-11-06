from flask import Flask, render_template, request, jsonify, send_file
import feedparser, requests, os, re
from urllib.parse import quote
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
APP_NAME = "SHIVANKVERSE AI NEWS AGENT"

FEEDS = [
    ("Google News · AI", "https://news.google.com/rss/search?q=artificial+intelligence+OR+AI+agents&hl=en-US&gl=US&ceid=US:en"),
    ("Google News · Chips", "https://news.google.com/rss/search?q=semiconductor+OR+GPU+OR+chip+breakthrough&hl=en-US&gl=US&ceid=US:en"),
    ("Google News · Robotics", "https://news.google.com/rss/search?q=robotics+OR+humanoid+robot&hl=en-US&gl=US&ceid=US:en"),
    ("Google News · Space", "https://news.google.com/rss/search?q=space+technology+OR+satellite+OR+rocket&hl=en-US&gl=US&ceid=US:en"),
    ("Google News · Quantum", "https://news.google.com/rss/search?q=quantum+computing+technology&hl=en-US&gl=US&ceid=US:en"),
]

def clean(s):
    return re.sub(r"<[^>]+>", "", str(s or "")).strip()

@app.get("/")
def home():
    return render_template("index.html", app_name=APP_NAME)

@app.get("/api/news")
def news():
    items, seen = [], set()
    for category, url in FEEDS:
        try:
            parsed = feedparser.parse(url)
            for e in parsed.entries[:12]:
                title = clean(e.get("title"))
                link = e.get("link", "")
                key = title.lower()
                if title and key not in seen:
                    seen.add(key)
                    items.append({
                        "title": title, "link": link, "category": category,
                        "published": clean(e.get("published", "")),
                        "summary": clean(e.get("summary", ""))[:450]
                    })
        except Exception:
            pass
    items.sort(key=lambda x: x["published"], reverse=True)
    return jsonify({"items": items[:40], "updated": datetime.now().strftime("%d %b %Y, %I:%M %p")})

@app.post("/api/draft")
def draft():
    data = request.get_json(force=True)
    title = clean(data.get("title"))
    source = clean(data.get("source"))
    notes = clean(data.get("notes"))
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("AI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.getenv("AI_MODEL", "gpt-4o-mini")
    if not title:
        return jsonify({"error": "Pehle news select karo."}), 400
    prompt = f"""You are the editorial assistant for SHIVANKVERSE, a Hindi technology news publication.
Write an original, factual Hindi/Hinglish SEO article based ONLY on the supplied information.
Do not invent facts, dates, numbers, quotes or claims. If information is missing, clearly say it needs verification.
Distinguish confirmed facts from analysis. Explain technical terms simply.
Return clean HTML using h2, h3, p, ul, li. Include headline, short intro, context, what happened, why it matters, limitations/what is not confirmed, India relevance, conclusion.
Story title: {title}
Source link: {source}
Additional notes: {notes}
"""
    if not api_key:
        html = f"""<h2>{title}</h2>
<p><b>संपादकीय नोट:</b> यह शुरुआती ड्राफ्ट है। प्रकाशित करने से पहले मूल स्रोत खोलकर सभी तथ्य, तारीख और दावों की पुष्टि करें।</p>
<h2>क्या हुआ?</h2><p>{title} से जुड़ी खबर पर अभी उपलब्ध शीर्षक के आधार पर यह ड्राफ्ट तैयार किया गया है। पूरी जानकारी और आधिकारिक पुष्टि के बिना अतिरिक्त तथ्य जोड़ना सही नहीं होगा।</p>
<h2>यह क्यों महत्वपूर्ण है?</h2><p>इस खबर का वास्तविक प्रभाव समझने के लिए तकनीक, इसकी उपलब्धता, लागत, सीमाएँ और उपयोग के मामलों की जाँच जरूरी है।</p>
<h2>भारत के लिए इसका क्या मतलब है?</h2><p>भारत में इसके संभावित उपयोग, स्थानीय कंपनियों और उपभोक्ताओं पर असर की पुष्टि विश्वसनीय स्रोतों से करें।</p>
<h2>निष्कर्ष</h2><p>अभी इसे प्रारंभिक खबर मानें। आधिकारिक घोषणा और कम-से-कम दो विश्वसनीय स्रोतों से पुष्टि के बाद ही प्रकाशित करें।</p>"""
        return jsonify({"html": html, "mode": "template", "notice": "AI API key नहीं मिली। सुरक्षित शुरुआती टेम्पलेट बनाया गया है; यह AI-generated fact-checked article नहीं है।"})
    try:
        r = requests.post(base_url + "/chat/completions",
            headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
            json={"model": model, "messages": [{"role":"user","content":prompt}], "temperature":0.4},
            timeout=90)
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]
        return jsonify({"html": content, "mode": "ai", "notice": "AI draft तैयार है। प्रकाशित करने से पहले स्रोतों से तथ्य जाँचें।"})
    except Exception as e:
        return jsonify({"error": "AI सेवा से जवाब नहीं मिला। API key, model और internet जाँचें।"}), 502

@app.post("/api/export")
def export():
    data = request.get_json(force=True)
    title = clean(data.get("title")) or "SHIVANKVERSE Article"
    body = data.get("html", "")
    html = f"""<!doctype html><html lang="hi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><article style="max-width:780px;margin:40px auto;padding:20px;font:18px/1.8 Arial,sans-serif"><h1>{title}</h1>{body}<hr><p>Source review: आवश्यक | SHIVANKVERSE</p></article></html>"""
    path = os.path.join(os.path.dirname(__file__), "article_export.html")
    with open(path, "w", encoding="utf-8") as f: f.write(html)
    return send_file(path, as_attachment=True, download_name="shivankverse-article.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=False)
