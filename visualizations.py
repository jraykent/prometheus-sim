import matplotlib.pyplot as plt

def plot_ideology_drift(personas):
    plt.figure(figsize=(8, 4))
    for p in personas:
        if p.log:
            plt.plot([entry['ideology'] for entry in p.log], label=p.name)
    plt.xlabel("Event #")
    plt.ylabel("Ideology")
    plt.title("Ideology Drift Over Time")
    plt.legend()
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

def plot_emotions_over_time(personas):
    plt.figure(figsize=(8, 4))
    for p in personas:
        if p.log:
            emotions = [entry['emotion'] for entry in p.log]
            plt.plot(emotions, label=p.name)
    plt.xlabel("Event #")
    plt.ylabel("Emotion")
    plt.title("Emotion Over Time (raw, for debugging)")
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
