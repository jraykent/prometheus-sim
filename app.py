def simulate_reaction(persona, headline, trust_step=0.01, ideology_chance=10):
    import random
    from datetime import datetime

    age = persona["age"]
    trust = persona.get("trust", 0.5)

    # Example: use trust_step from sidebar, not hardcoded
    if age <= 10:
        summary = "Doesn't understand it fully, feels uneasy."
        emotion = "confused/scared"
        trust_delta = -trust_step
    elif age <= 17:
        summary = "Feels personally affected, influenced by how others react."
        emotion = "anxious or excited"
        trust_delta = random.choice([-trust_step, trust_step])
    elif age <= 30:
        summary = "Curious and reactive, split on trust."
        emotion = "mixed"
        trust_delta = trust_step
    elif age <= 60:
        summary = "Wants facts and context before reacting."
        emotion = "skeptical"
        trust_delta = -trust_step
    else:
        summary = "Defaults to past experience and established media."
        emotion = "resigned or concerned"
        trust_delta = -2 * trust_step

    persona["trust"] = min(max(trust + trust_delta, 0), 1)

    # Use ideology_chance from sidebar
    if random.randint(1, 100) <= ideology_chance:
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

    persona.setdefault("belief_log", []).append({
        "headline": headline,
        "reaction": reaction
    })

    return reaction

def run_simulation(personas, headline, trust_step=0.01, ideology_chance=10):
    results = []
    for p in personas:
        reaction = simulate_reaction(p, headline, trust_step=trust_step, ideology_chance=ideology_chance)
        p["reaction"] = reaction
        results.append(p)
    save_state(personas)
    return results

def auto_run_news_simulation(trust_step=0.01, ideology_chance=10):
    personas = load_personas()
    headlines = get_live_headlines() + get_reddit_headlines()
    for headline in headlines:
        run_simulation(personas, headline, trust_step=trust_step, ideology_chance=ideology_chance)
    save_state(personas)
