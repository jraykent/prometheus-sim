import requests
import random

NEWSAPI_KEY = "YOUR_NEWSAPI_KEY"  # Replace with your real NewsAPI key

def fetch_newsapi_headlines(topic='general', max_results=10):
    url = f"https://newsapi.org/v2/top-headlines?category={topic}&language=en&pageSize={max_results}&apiKey={NEWSAPI_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        articles = r.json().get('articles', [])
        return [(a['title'], topic, random.uniform(-1,1)) for a in articles]
    return []

def get_sample_headlines():
    samples = [
        ("Economy hits record growth", "economy", 0.8),
        ("Political tensions rise in Congress", "politics", -0.7),
        ("New tech revolutionizes classrooms", "tech", 0.6),
        ("Celebrity scandal shocks nation", "social", -0.8),
        ("Breakthrough in cancer treatment", "health", 0.9),
    ]
    return samples

def generate_synthetic_headline():
    topics = ['economy', 'politics', 'tech', 'health', 'social']
    sentiments = [-0.8, -0.4, 0, 0.4, 0.8]
    return (f"AI disrupts {random.choice(topics)} sector", random.choice(topics), random.choice(sentiments))

# GPT-powered analysis (optional)
def gpt_headline_analysis(headline, topic, interests, api_key=None):
    import openai
    if api_key:
        openai.api_key = api_key
    prompt = (f"Headline: '{headline}'\n"
              f"Topic: {topic}\n"
              f"Persona interests: {', '.join(interests)}\n"
              f"Analyze: Sentiment (-1 to 1), Bias (-1=left, 1=right), "
              "Does this confirm or challenge the persona's beliefs? Is it misleading?\n"
              "Respond in JSON with keys: sentiment, bias, subtext.")
    response = openai.ChatCompletion.create(
        model="gpt-4o", messages=[{"role":"user","content":prompt}]
    )
    import json
    try:
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {"sentiment": 0, "bias": 0, "subtext": "No strong effect"}
