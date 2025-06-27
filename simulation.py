import time
import random

def run_simulation(personas, headlines, steps=10, api_func=None, auto_learn=True):
    for i in range(steps):
        headline, topic = random.choice(headlines)[:2]
        nlp_results = []
        for persona in personas:
            nlp_results.append(persona.nlp_headline_analysis(headline, topic, api_func=api_func))
        for idx, persona in enumerate(personas):
            peers = [p for p in personas if p is not persona and abs(p.age-persona.age)<12]
            if peers:
                peer_influence = (sum([p.ideology for p in peers])/len(peers))-persona.ideology
            else:
                peer_influence = 0
            persona.react(headline, topic, nlp_results[idx], peer_influence=peer_influence)
            if auto_learn:
                persona.auto_learn()
        time.sleep(0.05)

def run_blackbox(personas, adversarial_headlines, steps=10):
    for i in range(steps):
        headline = random.choice(adversarial_headlines)
        for persona in personas:
            persona.react(*headline)
            persona.auto_learn()
        time.sleep(0.05)
