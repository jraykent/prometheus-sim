import json
import os
import random
import requests
from datetime import datetime

LOG_DIR = "logs"
STATE_FILE = os.path.join(LOG_DIR, "personas_state.json")

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

def sentiment_score(headline):
    negative = ["loss", "fire", "death", "strike", "cyberattack", "outage", "shooting", "ban", "attack", "seize", "danger"]
    positive = ["breakthrough", "improvement", "treat", "saves", "recovery", "record", "acquitted", "win", "rescued", "growth"]
    headline_l = headline.lower()
    if any(word in headline_l for word in negative):
        return -1
    if any(word in headline_l for word in positive):
        return 1
    return 0

def emotion_by_headline(headline, persona):
    h = headline.lower()
    if "fire" in h or "death" in h or "attack" in h or "shooting" in h:
        return "scared"
    elif "court" in h or "ban" in h or "politics" in h:
        return "angry"
    elif "breakthrough" in h or "improve" in h or "record" in h:
        return "hopeful"
    if len(persona["belief_log"]) > 20 and all(
        e["headline"] == headline for e in persona["belief_log"][-5:]
    ):
        return "numb"
    return "neutral"

def nudge_ideology(persona, headline):
    # Only for adults/teens
    if persona["age"] < 14:
        return
    h = headline.lower()
    if "court" in h or "ban" in h or "supreme" in h:
        persona["ideology"] = random.choice(["liberal", "conservative"])
    elif "congress" in h or "house" in h or "democrat" in h:
        persona["ideology"] = "liberal"
    elif "republican" in h or "fox news" in h or "trump" in h:
        persona["ideology"] = "conservative"
    # Small chance to drift
    elif random.random() < 0.05:
        persona["ideology"] = random.choice(["liberal", "conservative", "centrist", "unknown"])

def simulate_reaction(persona, headline, trust_step=0.01, ideology_chance=10):
    age = persona["age"]
    trust = persona.get("trust", 0.5)
    sentiment = sentiment_score(headline)
    burnout = min(len(persona['belief_log']) / 100, 0.5)  # maxes at 0.5

    # Smarter trust delta by age/sentiment/burnout
    if age <= 10:
        summary = "Doesn't understand it fully, feels uneasy."
        emotion = "confused/scared"
        trust_delta = -trust_step * (1 + abs(sentiment)) * (1 - burnout)
    elif age <= 17:
        summary = "Feels personally affected, influenced by how others react."
        emotion = emotion_by_headline(headline, persona)
        trust_delta = trust_step * sentiment * (1 - burnout) + random.choice([-trust_step, trust_step]) * 0.2
    elif age <= 30:
        summary = "Curious, reactive, identity-seeking."
        emotion = emotion_by_headline(headline, persona)
        trust_delta = trust_step * sentiment * 1.5 * (1 - burnout)
    elif age <= 60:
        summary = "Wants facts/context; influenced by repetition."
        emotion = emotion_by_headline(headline, persona)
        trust_delta = trust_step * sentiment * (0.75 if burnout > 0.3 else 1)
    else:
        summary = "Defaults to experience, slow to change."
        emotion = "resigned" if sentiment == -1 else "concerned"
        trust_delta = -0.5 * trust_step * (1 - burnout)

    persona["trust"] = round(min(max(trust + trust_delta, 0), 1), 2)

    # Ideology change: age/logic/exposure
    if random.randint(1, 100) <= ideology_chance:
        nudge_ideology(persona, headline)

    reaction = {
        "summary": summary,
        "emotion": emotion,
        "trust_level": round(persona["trust"], 2),
        "ideology": persona.get("ideology", "unknown"),
        "note": f"{persona['name']} responded to: {headline}",
        "timestamp": datetime.now().isoformat()
    }

    persona.setdefault("belief_log", []).append({
        "headline": headline,
        "reaction": reaction
    })

    return reaction

def contagion(personas):
    # If >50% share an ideology, 20% chance others follow
    id_counts = {}
    for p in personas:
        id_counts[p["ideology"]] = id_counts.get(p["ideology"], 0) + 1
    majority = max(id_counts, key=id_counts.get)
    if id_counts[majority] > len(personas) // 2:
        for p in personas:
            if p["ideology"] != majority and random.random() < 0.2:
                p["ideology"] = majority

def run_simulation(personas, headline, trust_step=0.01, ideology_chance=10):
    results = []
    for p in personas:
        reaction = simulate_reaction(
            p, headline, trust_step=trust_step, ideology_chance=ideology_chance
        )
        p["reaction"] = reaction
        results.append(p)
    contagion(personas)
    save_state(personas)
    return results

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

def auto_run_news_simulation(trust_step=0.01, ideology_chance=10):
    personas = load_personas()
    headlines = get_live_headlines() + get_reddit_headlines()
    for headline in headlines:
        run_simulation(personas, headline, trust_step=trust_step, ideology_chance=ideology_chance)
    save_state(personas)
