import pandas as pd

def compute_drift(persona):
    log = persona.log
    if not log or len(log) < 2:
        return 0
    return log[-1]['ideology'] - log[0]['ideology']

def compute_trust_range(persona):
    log = persona.log
    if not log or len(log) < 2:
        return 0
    trusts = [l['trust'] for l in log]
    return max(trusts) - min(trusts)

def summarize_all(personas):
    return pd.DataFrame([p.summary() for p in personas])

def logs_to_dataframe(personas):
    frames = []
    for p in personas:
        df = p.export_log()
        df['persona'] = p.name
        frames.append(df)
    if frames:
        return pd.concat(frames, ignore_index=True)
    return pd.DataFrame()
