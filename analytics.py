import pandas as pd

def compute_drift(persona):
    log = persona.log
    if not log or len(log) < 2:
        return 0
    return log[-1]['ideology'] - log[0]['ideology']

def compute_polarization(personas):
    return max(abs(p.ideology) for p in personas) - min(p.ideology for p in personas)

def summarize_all(personas):
    return pd.DataFrame([p.summary() for p in personas])
