# persona_engine.py — Prometheus Core Logic

from datetime import datetime
import json
import os

# ===== Persona Definitions (Age Range: 6–75) =====
personas = [
    {"name": "Lily", "age": 6, "media_habits": ["YouTube Kids"], "emotional_profile": "Curious, sensitive", "cognitive_traits": ["literal thinker"], "belief_log": []},
    {"name": "Aiden", "age": 13, "media_habits": ["TikTok", "YouTube"], "emotional_profile": "Impressionable, reactive", "cognitive_traits": ["peer-influenced"], "belief_log": []},
    {"name": "Chloe", "age": 18, "media_habits": ["Snapchat", "Instagram"], "emotional_profile": "Exploratory, values identity", "cognitive_traits": ["tribal alignment"], "belief_log": []},
    {"name": "Noah", "age": 25, "media_habits": ["Reddit", "X/Twitter"], "emotional_profile": "Cynical, analytical", "cognitive_traits": ["confirmation-seeking"], "belief_log": []},
    {"name": "Marcus", "age": 38, "media_habits": ["NPR", "X/Twitter"], "emotional_profile": "Stability-focused", "cognitive_traits": ["skeptical of trends"], "belief_log": []},
    {"name": "Elaine", "age": 52, "media_habits": ["Facebook", "Fox News"], "emotional_profile": "Security-minded", "cognitive_traits": ["fears change"], "belief_log": []},
    {"name": "Walter", "age": 75, "media_habits": ["TV news", "local paper"], "emotional_profile": "Traditionalist, routine-bound", "cognitive_traits": ["values consistency"], "belief_log": []}
]

# ===== Simulated Reaction Engine =====
def simulate_reaction(persona, headline):
    age = persona["age"]
    if age < 10:
        summary = "Doesn't understand it fully, feels uneasy."
        emotion = "confused/scared"
        trust = "low"
    elif age < 20:
        summary = "Feels personally affected, influenced by how others react."
        emotion = "anxious or excited"
        trust = "shifting"
    elif age < 35:
        summary = "Curious and reactive, split on trust."
        emotion = "mixed"
        trust = "medium"
    elif age < 60:
        summary = "Wants facts and context before reacting."
        emotion = "skeptical"
        trust = "moderate"
    else:
        summary = "Defaults to past experience and established media."
        emotion = "resigned or concerned"
        trust = "low to moderate"

    response = {
        "summary": summary,
        "emotion": emotion,
        "trust_level": trust,
        "note": f"Responds based on age {age} persona filter."
    }

    persona["belief_log"].append({
        "timestamp": datetime.now().isoformat(),
        "headline": headline,
        "reaction": response
    })

    return response

# ===== Load & Save Functions =====
def load_personas():
    return personas

def run_simulation(personas, headline):
    results = []
    for p in personas:
        reaction = simulate_reaction(p, headline)
        results.append({"name": p["name"], "age": p["age"], "reaction": reaction})
    return results

def save_state():
    os.makedirs("logs", exist_ok=True)
    with open("logs/personas_state.json", "w") as f:
        json.dump(personas, f, indent=2)

