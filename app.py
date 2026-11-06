import os, re
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
import feedparser, requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
FEEDS = [
 ("AI & AI Agents", "https://news.google.com/rss/search?q=AI+agents+OR+artificial+intelligence&hl=en-US&gl=US&ceid=US:en"),
 ("Chips & Semiconductors", "https://news.google.com/rss/search?q=semiconductor+OR+GPU+OR+chip+technology&hl=en-US&gl=US&ceid=US:en"),
 ("Robotics", "https://news.google.com/rss/search?q=robotics+OR+humanoid+robots&hl=en-US&gl=US&ceid=US:en"),
 ("Space Technology", "https://news.google.com/rss/search?q=space+technology+OR+satellite+OR+rocket&hl=en-US&gl=US&ceid=US:en"),
 ("Quantum", "https://news.google.com/rss/search?q=quantum+computing&hl=en-US&gl=US&ceid=US:en")
]
def clean(v):
    return re.sub(r"<[^>]*>", "", str(v or "")).strip()

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/news")
def get_news():
    out, seen = [], set()
    for category, url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:15]:
                title = clean(entry.get("title"))
                if not title or title.lower() in seen: continue
                seen.add(title.lower())
                out.append({"title":title, "link":entry.get("link",""),
                            "category":category, "published":clean(entry.get("published","")),
                            "summary":clean(entry.get("summary",""))[:400]})
        except Exception:
            continue
    out.sort(key=lambda x:x["published"], reverse=True)
    return jsonify({"items":out[:50], "updated":datetime.now().strftime("%d %b %Y %H:%M")})

@app.post("/api/draft")
def draft():
    data=request.get_json(force=True)
    title=clean(data.get("title"))
    source=clean(data.get("source"))
    notes=clean(data.get("notes"))
    if not title: return jsonify({"error":"Pehle news select karo."}),400
    key=os.getenv("OPENAI_API_KEY","").strip()
    base_url=os.getenv("AI_BASE_URL","https://api.openai.com/v1").rstrip("/")
    model=os.getenv("AI_MODEL","gpt-4o-mini")
    if not key:
        html=f"""<h2>{title}</h2><p><b>संपादकीय नोट:</b> यह केवल शुरुआती ढाँचा है। प्रकाशित करने से पहले मूल स्रोत और सभी तथ्य जाँचें।</p><h2>क्या हुआ?</h2><p>इस खबर के बारे में उपलब्ध जानकारी और आधिकारिक घोषणा को यहाँ विस्तार से लिखें।</p><h2>यह क्यों महत्वपूर्ण है?</h2><p>इस तकनीक का महत्व, संभावित उपयोग और इसकी सीमाएँ समझाएँ।</p><h2>भारत पर संभावित असर</h2><p>भारत के उपयोगकर्ताओं, उद्योग और तकनीकी क्षेत्र पर संभावित प्रभाव की पुष्टि करें।</p><h2>निष्कर्ष</h2><p>विश्वसनीय स्रोतों से पुष्टि के बाद ही अंतिम लेख प्रकाशित करें।</p>"""
        return jsonify({"html":html,"notice":"AI API key नहीं मिली। यह template है, AI fact-check या पूर्ण लेख नहीं।"})
    prompt=f"""Write an original Hindi/Hinglish SEO technology news article for SHIVANKVERSE using ONLY supplied facts. Do not invent details. Clearly mark unverified information and distinguish announcement, research, prototype and availability. Use HTML h2,h3,p,ul,li. Explain technical terms simply. Include what happened, context, why it matters, limitations, India relevance and conclusion.
Headline: {title}
Source URL: {source}
Verified notes: {notes}"""
    try:
        res=requests.post(base_url+"/chat/completions",
          headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},
          json={"model":model,"messages":[{"role":"user","content":prompt}],"temperature":0.3},timeout=90)
        res.raise_for_status()
        article=res.json()["choices"][0]["message"]["content"]
        return jsonify({"html":article,"notice":"AI draft तैयार है। publish करने से पहले मूल स्रोतों से जाँचें।"})
    except Exception:
        return jsonify({"error":"AI API call असफल। API key, model और provider settings जाँचें।"}),502

@app.post("/api/export")
def export():
    data=request.get_json(force=True)
    title=clean(data.get("title")) or "SHIVANKVERSE Article"
    body=data.get("html","")
    path=os.path.join(os.path.dirname(__file__),"article_export.html")
    with open(path,"w",encoding="utf-8") as f:
        f.write(f'<!doctype html><html lang="hi"><meta charset="utf-8"><title>{title}</title><article><h1>{title}</h1>{body}</article></html>')
    return send_file(path,as_attachment=True,download_name="shivankverse-article.html")

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
