import requests
import random

# NewsAPI and Reddit credentials here
NEWSAPI_KEY = "5407bb8bb38b433b8f9973bf024e2f61"

def fetch_newsapi_headlines(topic='general', max_results=10):
    url = f"https://newsapi.org/v2/top-headlines?category={topic}&language=en&pageSize={max_results}&apiKey={NEWSAPI_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        articles = r.json().get('articles', [])
        return [(a['title'], topic, random.uniform(-1,1), random.uniform(0,1)) for a in articles]
    return []

def fetch_reddit_headlines(subreddit="news", max_results=10):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={max_results}"
    headers = {"User-Agent": "PrometheusSim/0.1"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        posts = data["data"]["children"]
        return [(p["data"]["title"], subreddit, random.uniform(-1,1), random.uniform(0,1)) for p in posts]
    return []

def get_sample_headlines():
    return [
        ("Major earthquake strikes city", "disaster", -0.8, 0.9),
        ("School opens new playground", "school", 0.6, 0.4),
        ("Election results spark protests", "politics", -0.7, 0.7),
        ("Medical breakthrough in cancer treatment", "health", 0.85, 0.8),
        ("Celebrity wins humanitarian award", "social", 0.5, 0.3),
        ("Rumors of economic downturn", "economy", -0.6, 0.5),
        ("Community hosts festival", "community", 0.3, 0.3)
    ]

def generate_synthetic_headline():
    topics = ['economy', 'politics', 'tech', 'health', 'social']
    sentiments = [-0.8, -0.4, 0, 0.4, 0.8]
    return (f"AI disrupts {random.choice(topics)} sector", random.choice(topics), random.choice(sentiments), random.uniform(0,1))

# GPT headline analysis (optional)
def gpt_headline_analysis(headline, topic, interests, api_key=None):
    import openai
    if api_key:
        openai.api_key = api_key
    prompt = (f"Headline: '{headline}'\n"
              f"Topic: {topic}\n"
              f"Persona interests: {', '.join(interests)}\n"
              f"Analyze: Sentiment (-1 to 1), Surprise (0 to 1), Is this misleading? Respond in JSON with keys: sentiment, surprise, subtext.")
    response = openai.ChatCompletion.create(
        model="gpt-4o", messages=[{"role":"user","content":prompt}]
    )
    import json
    try:
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {"sentiment": 0, "surprise": 0.5, "subtext": "No strong effect"}
