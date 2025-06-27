import random
import time

def run_simulation(personas, headlines, steps=10, api_func=None, auto_learn=True):
    for i in range(steps):
        event = random.choice(headlines)
        nlp_results = []
        for persona in personas:
            if api_func:
                nlp = persona.nlp_headline_analysis(event[0], event[1], api_func=api_func)
                nlp_results.append((event[0], event[1], nlp['sentiment'], nlp['surprise']))
            else:
                nlp_results.append(event)
        peer_ideologies = [p.ideology for p in personas]
        for idx, persona in enumerate(personas):
            peer_mean = sum(peer_ideologies)/len(peer_ideologies)
            peer_influence = (peer_mean - persona.ideology) * 0.2
            persona.react(*nlp_results[idx], peer_influence=peer_influence)
            if auto_learn:
                persona.recover()
        time.sleep(0.01)

def run_blackbox(personas, adversarial_headlines, steps=10):
    for i in range(steps):
        event = random.choice(adversarial_headlines)
        for persona in personas:
            persona.react(*event)
            persona.recover()
        time.sleep(0.01)
