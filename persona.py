import random
import numpy as np
from collections import deque, defaultdict

PERSONALITY_TRAITS = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]

def random_personality():
    return {trait: np.clip(np.random.normal(0.5, 0.18), 0, 1) for trait in PERSONALITY_TRAITS}

def age_bracket(age):
    if age < 13: return "child"
    if age < 20: return "teen"
    if age < 60: return "adult"
    return "senior"

EMOTIONS_BY_AGE = {
    "child": ["scared", "curious", "confused", "happy", "sad", "bored"],
    "teen": ["anxious", "excited", "indifferent", "angry", "hopeful", "bored"],
    "adult": ["concerned", "hopeful", "cynical", "confident", "bored", "calm"],
    "senior": ["nostalgic", "resigned", "hopeful", "concerned", "proud", "bored"]
}

def get_emotion_for_event(age, valence, surprise):
    bracket = age_bracket(age)
    emo_pool = EMOTIONS_BY_AGE[bracket]
    if valence > 0.5:
        return "happy" if "happy" in emo_pool else "hopeful"
    if valence < -0.5:
        if surprise > 0.5:
            return "scared" if "scared" in emo_pool else "anxious"
        return "sad" if "sad" in emo_pool else "concerned"
    if abs(valence) < 0.15 and surprise > 0.7:
        return "curious"
    if abs(valence) < 0.15:
        return "bored"
    return random.choice(emo_pool)

class Persona:
    def __init__(self, name, age, ideology=0.0, trust=0.5, personality=None, digital_literacy=None):
        self.name = name
        self.age = age
        self.ideology = ideology # -1 to +1, left to right
        self.trust = trust # 0 to 1
        self.emotion = "calm"
        self.personality = personality or random_personality()
        self.digital_literacy = digital_literacy if digital_literacy is not None else np.clip(np.random.normal(0.5, 0.2), 0, 1)
        self.interests = self._default_interests()
        self.memory = deque(maxlen=75)
        self.topic_exposure = defaultdict(int)
        self.log = []
        self.habituation = 0.06 + (0.04 * (1 - self.personality["openness"]))
        self.recovery_rate = 0.04 + (0.04 * self.personality["conscientiousness"])
        self.susceptibility = 0.14 + (0.13 * (1 - self.personality["openness"]))
        self.positivity = 0.5 + 0.3 * self.personality["agreeableness"]
        self.neuroticism = self.personality["neuroticism"]

    def _default_interests(self):
        if self.age < 13:
            return ["cartoons", "games", "family"]
        if self.age < 20:
            return ["music", "trends", "friends"]
        if self.age < 60:
            return ["news", "work", "technology", "health"]
        return ["health", "family", "history", "security"]

    def react(self, headline, topic, valence, surprise, topic_bias=0.0, peer_influence=0.0):
        exp = self.topic_exposure[topic]
        habit_factor = max(0.2, 1 - exp * self.habituation)
        interest_factor = 1.3 if topic in self.interests else 1.0
        emotionality = 0.6 + 0.7 * self.neuroticism

        net_valence = (valence * interest_factor * habit_factor) + (0.1 * topic_bias)
        net_valence += peer_influence * 0.2
        surprise = min(max(surprise, 0), 1)
        self.emotion = get_emotion_for_event(self.age, net_valence, surprise)

        # Trust logic
        prev_trust = self.trust
        trust_shift = 0.025 * net_valence * emotionality
        if "misinfo" in headline.lower():
            trust_shift -= 0.07 * (1 - self.personality["conscientiousness"])
        if net_valence > 0.2 and self.trust < 1:
            trust_shift += 0.012 * self.positivity
        self.trust = np.clip(self.trust + trust_shift, 0, 1)

        # Ideology logic
        if topic in ["politics", "world", "social"]:
            drift = net_valence * 0.05 * (1 + self.personality["openness"]) * (1 - abs(self.ideology))
            self.ideology = np.clip(self.ideology + drift, -1, 1)

        # Memory
        self.memory.append((headline, topic, valence, net_valence, self.emotion, self.trust, self.ideology))
        self.topic_exposure[topic] += 1

        # Log
        self.log.append({
            "headline": headline,
            "topic": topic,
            "valence": valence,
            "surprise": surprise,
            "emotion": self.emotion,
            "trust": self.trust,
            "ideology": self.ideology,
            "exposure": self.topic_exposure[topic],
            "interest": topic in self.interests,
            "peer_influence": peer_influence,
            "personality": self.personality.copy()
        })

    def recover(self):
        if self.emotion in ("scared", "anxious", "sad", "confused", "angry", "outraged"):
            if random.random() < 0.75:
                self.emotion = "calm"
        self.trust += (0.5 - self.trust) * self.recovery_rate
        self.trust = np.clip(self.trust, 0, 1)
        self.ideology *= (1 - self.recovery_rate / 2)

    def summary(self):
        return {
            "name": self.name,
            "age": self.age,
            "ideology": round(self.ideology, 2),
            "trust": round(self.trust, 2),
            "emotion": self.emotion,
            "top_interest": max(self.topic_exposure, key=self.topic_exposure.get, default=None)
        }

    def explain(self):
        mood = f"{self.name} ({self.age}) is feeling {self.emotion}."
        trust = f"Trust: {self.trust:.2f} | Ideology: {self.ideology:.2f}."
        dominant = f"Most exposed topic: {self.summary()['top_interest'] or 'N/A'}."
        return f"{mood} {trust} {dominant}"

    def export_log(self):
        import pandas as pd
        return pd.DataFrame(self.log)
