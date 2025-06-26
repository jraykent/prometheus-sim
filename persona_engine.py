import json
import os
from datetime import datetime
import random
import requests

LOG_DIR = "logs"
STATE_FILE = os.path.join(LOG_DIR, "personas_state.json")
LOG_FILE = os.path.join(LOG_DIR, "persona_log.json")

DEFAULT_PERSONAS = [
    {
        "name": "Lily",
        "age": 6,
        "trust": 0.5,
        "ideology": "unknown",
        "belief_log": []
    },
    {
        "name": "Aiden",
        "age": 13,
        "trust": 0.4,
        "ideology": "unknown",
        "belief_log": []
    },
    {
        "name": "Chloe",
        "age": 18,
        "trust": 0.6,
        "ideology": "unknown",
        "belief_log": []
    },
    {
        "name": "Noah",
        "age": 25,
        "trust": 0.7,
        "ideology": "unknown",
        "belief_log": []
    },
    {
        "name": "Marcus",
        "age": 38,
        "trust": 0.8,
        "ideology": "unknown",
        "belief_log": []
    },
    {
        "name": "Elaine",
        "age": 52,
        "trust": 0.65,
        "ideology": "unknown",
        "belief_log": []
    },
    {
        "name": "Walter",
        "age": 75,
        "trust": 0.55,
        "ideology": "unknown",
        "belief_log": []
    }
]

def load_personas():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    else:
        return DEFAULT_PERSONAS.copy()

def save_state(personas=None):
    os.makedirs(LOG_DIR, exist_ok=True)
    if personas is None:
        personas = load_personas()
    with open(STATE_FILE, "w") as f:
        json.dump(personas, f, indent=2)

def simulate_reaction(persona, headline):
    # "Learn" slightly: trust drifts, belief log grows, possible ideology shift
    reaction = {}
    age = persona["age"]
    trust = persona.get("trust", 0.5)

    if age <= 10:
        summary = "Doesn't understand it fully, feels uneasy."
        emotion = "confused/scared"
        trust_delta = -0.01
    elif age <= 17:
        summary = "Feels personally affected, influenced by how others react."
        emotion = "anxious or excited"
        trust_delta = random.choice([-0.01, 0.01])
    elif age <= 30:
        summary = "Curious and reactive, split on trust."
        emotion = "mixed"
        trust_delta = 0.01
    elif age <= 60:
        summary = "Wants facts and context before reacting."
        emotion = "skeptical"
        trust_delta = -0.01
    else:
        summary = "Defaults to past experience and established media."
        emotion = "resigned or concerned"
        trust_delta = -0.02

    # Evolve trust
    persona["trust"] = min(max(trust + trust_delta, 0), 1)

    # Optional: simplistic ideology drift (random, but you can expand)
    if random.random() < 0.1:  # 10% chance to shift
        persona["ideology"] = random.choice(
            ["liberal", "conservative", "centrist", "unknown"]
        )

    reaction = {
        "summary": summary,
        "emotion": emotion,
        "trust_level": round(persona["trust"], 2),
        "ideology": persona.get("ideology", "unknown"),
        "note": f"{persona['name']} responded to: {headline}",
        "timestamp": datetime.now().isoformat()
    }

    # Save reaction in memory
    persona.setdefault("belief_log", []).append({
        "headline": headline,
        "reaction": reaction
    })

    return reaction

def run_simulation(personas, headline):
    results = []
    for p in personas:
        reaction = simulate_reaction(p, headline)
        p["reaction"] = reaction
        results.append(p)
    save_state(personas)
    return results

# ----------- NEW: Live News and Reddit Feeds ------------

def get_live_headlines():
    api_key = "5407bb8bb38b433b8f9973bf024e2f61"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    resp = requests.get(url)
    headlines = []
    if resp.status_code == 200:
        data = resp.json()
        for article in data.get("articles", []):
            headlines.append(article["title"])
    return headlines[:10] if headlines else ["[NewsAPI ERROR]"]

def get_reddit_headlines():
    url = "https://www.reddit.com/r/news/top.json?limit=10&t=day"
    headers = {'User-agent': 'PrometheusBot/0.1'}
    resp = requests.get(url, headers=headers)
    headlines = []
    if resp.status_code == 200:
        data = resp.json()
        for post in data["data"]["children"]:
            headlines.append(post["data"]["title"])
    return headlines[:10] if headlines else ["[Reddit ERROR]"]

def auto_run_news_simulation():
    personas = load_personas()
    headlines = get_live_headlines() + get_reddit_headlines()
    for headline in headlines:
        run_simulation(personas, headline)
    save_state(personas)
