import matplotlib.pyplot as plt

def plot_ideology_drift(personas):
    plt.figure(figsize=(8, 4))
    for p in personas:
        if p.log:
            plt.plot([entry['ideology'] for entry in p.log], label=p.name)
    plt.xlabel("Event #")
    plt.ylabel("Ideology (-1 = Left, 0 = Center, 1 = Right)")
    plt.title("Ideology Drift Over Time")
    plt.legend()
    plt.tight_layout()
    return plt

def plot_ideology_histogram(personas):
    values = [p.ideology for p in personas]
    plt.figure(figsize=(7, 3))
    plt.hist(values, bins=9, range=(-1, 1), edgecolor='k')
    plt.xlabel("Ideology (-1 = Left, 1 = Right)")
    plt.ylabel("Number of Personas")
    plt.title("Current Political Spectrum")
    plt.tight_layout()
    return plt

def plot_trust(personas):
    plt.figure(figsize=(8, 4))
    for p in personas:
        if p.log:
            plt.plot([entry['trust'] for entry in p.log], label=p.name)
    plt.xlabel("Event #")
    plt.ylabel("Trust Level")
    plt.title("Trust Level Over Time")
    plt.legend()
    plt.tight_layout()
    return plt

def plot_emotion_distribution(personas):
    import collections
    emotion_counts = collections.Counter()
    for p in personas:
        for e in p.log:
            emotion_counts[e['emotion']] += 1
    labels, values = zip(*emotion_counts.items()) if emotion_counts else ([], [])
    plt.figure(figsize=(7, 3))
    plt.bar(labels, values)
    plt.title("Emotion Distribution")
    plt.tight_layout()
    return plt
