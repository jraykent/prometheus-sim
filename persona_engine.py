import json
import os
from datetime import datetime
import random

PERSONA_FILE = "personas.json"
LOG_DIR = "logs"
STATE_FILE = os.path.join(LOG_DIR, "personas_state.json")
LOG_FILE = os.path.join(LOG_DIR, "persona_log.json")


# Sample personas
def load_personas():
    return [
        {"name": "Lily", "age": 6, "baseline_trust": 0.5},
        {"name": "Aiden", "age": 13, "baseline_trust": 0.4},
        {"name": "Chloe", "age": 18, "baseline_trust": 0.6},
        {"name": "Noah", "age": 25, "baseline_trust": 0.7},
        {"name": "Marcus", "age": 38, "baseline_trust": 0.8},
        {"name": "Elaine", "age": 52, "baseline_trust": 0.65},
        {"name": "Walter", "age": 75, "baseline_trust": 0.55},
    ]


def simulate_reaction(persona, headline):
    age = persona['age']
    name = persona['name']
    base_trust = persona['baseline_trust']

    if age <= 10:
        summary = "Doesn't understand it fully, feels uneasy."
        emotion = "confused/scared"
        trust = "low"
    elif age <= 17:
        summary = "Feels personally affected, influenced by how others react."
        emotion = "anxious or excited"
        trust = "shifting"
    elif age <= 30:
        summary = "Curious and reactive, split on trust."
        emotion = "mixed"
        trust = "medium"
    elif age <= 60:
        summary = "Wants facts and context before reacting."
        emotion = "skeptical"
        trust = "moderate"
    else:
        summary = "Defaults to past experience and established media."
        emotion = "resigned or concerned"
        trust = "low to moderate"

    return {
        "summary": summary,
        "emotion": emotion,
        "trust_level": trust,
        "ideology": persona.get("ideology", "unknown"),
        "note": f"{name} responded to: {headline}",
        "timestamp": datetime.now().isoformat()
    }


def run_simulation(personas, headline):
    results = []
    for p in personas:
        reaction = simulate_reaction(p, headline)
        p['reaction'] = reaction
        results.append(p)
    return results


def save_state(results=None):
    os.makedirs(LOG_DIR, exist_ok=True)
    if results:
        with open(STATE_FILE, "w") as f:
            json.dump(results, f, indent=2)
        with open(LOG_FILE, "a") as f:
            for r in results:
                json.dump(r, f)
                f.write("\n")


def auto_run_news_simulation():
    # Placeholder: Replace with real news scraping logic
    headlines = [
        "Supreme Court strikes down federal ban on bump stocks",
        "Major social media platform experiences global outage",
        "Breakthrough in cancer treatment shows 90% success rate",
    ]
    headline = random.choice(headlines)
    personas = load_personas()
    results = run_simulation(personas, headline)
    save_state(results)
