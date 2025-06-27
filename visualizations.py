import matplotlib.pyplot as plt

def plot_ideology_drift(personas):
    plt.figure(figsize=(8, 4))
    for p in personas:
        if p.log:
            plt.plot([e['ideology'] for e in p.log], label=p.name)
    plt.title("Ideology Drift")
    plt.xlabel("Events")
    plt.ylabel("Ideology")
    plt.legend()
    plt.tight_layout()
    return plt

def plot_emotion_distribution(personas):
    plt.figure(figsize=(7, 3))
    emotion_counts = {}
    for p in personas:
        for e in p.log:
            emotion = e['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    if emotion_counts:
        labels, values = zip(*emotion_counts.items())
        plt.bar(labels, values)
    plt.title("Emotion Distribution")
    plt.tight_layout()
    return plt
