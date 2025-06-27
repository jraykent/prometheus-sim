import random
import time

def run_simulation(personas, headlines, steps=10, auto_learn=True):
    for i in range(steps):
        event = random.choice(headlines)
        peer_ideologies = [p.ideology for p in personas]
        for idx, persona in enumerate(personas):
            peer_mean = sum(peer_ideologies) / len(peer_ideologies)
            peer_influence = (peer_mean - persona.ideology) * 0.2
            persona.react(*event, peer_influence=peer_influence)
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
