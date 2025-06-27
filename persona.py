import random
from collections import deque, defaultdict
import numpy as np

BIG_FIVE_TRAITS = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']

def random_traits():
    return {trait: np.clip(np.random.normal(0.5, 0.2), 0, 1) for trait in BIG_FIVE_TRAITS}

class Persona:
    def __init__(self, name, age, base_ideology=0.0, base_trust=0.5, interests=None,
                 personality=None, digital_literacy=None, social_circle=None):
        self.name = name
        self.age = age
        self.ideology = base_ideology
        self.trust = base_trust
        self.core_beliefs = base_ideology
        self.memory = deque(maxlen=200)
        self.interests = interests or self.default_interests()
        self.emotion = 'neutral'
        self.topic_exposure = defaultdict(int)
        self.polarization = 0.03 + (age / 80) * 0.05
        self.volatility = max(0.1, 1.1 - (age / 80))
        self.recovery = 0.1 if age < 22 else 0.04
        self.habituation = 0.35 if age < 18 else 0.18
        self.bias_tolerance = 0.7 if age < 30 else 0.4
        self.personality = personality or random_traits()
        self.digital_literacy = digital_literacy if digital_literacy is not None else np.clip(np.random.normal(0.5,0.2), 0, 1)
        self.media_habits = random.choices(['mainstream', 'alt', 'social'], weights=[0.5,0.2,0.3], k=2)
        self.social_circle = social_circle or []
        self.log = []
        self.misinformation_exposure = 0

    def default_interests(self):
        if self.age < 12:
            return ['games', 'school', 'cartoons']
        elif self.age < 18:
            return ['music', 'social', 'trends', 'school']
        elif self.age < 30:
            return ['politics', 'tech', 'work', 'culture']
        elif self.age < 55:
            return ['finance', 'politics', 'world', 'health']
        else:
            return ['politics', 'health', 'family', 'security']

    def _decay_memory(self):
        for i, (headline, topic, sentiment, impact, emotion, timestamp) in enumerate(self.memory):
            decay = 0.99 ** (len(self.memory)-i)
            self.memory[i] = (headline, topic, sentiment*decay, impact*decay, emotion, timestamp)

    def nlp_headline_analysis(self, headline, topic, api_func=None):
        if api_func:
            return api_func(headline, topic, self.interests)
        subtext = "This challenges your worldview" if random.random()<0.2 else "Confirms your priors"
        bias = np.clip(np.random.normal(0,0.4), -1, 1)
        sentiment = np.clip(np.random.normal(0,1), -1, 1)
        return {"sentiment": sentiment, "bias": bias, "subtext": subtext}

    def react(self, headline, topic, nlp_result, peer_influence=0.0):
        exposure = self.topic_exposure[topic]
        interest_boost = 1.3 if topic in self.interests else 1.0
        habituation_factor = np.exp(-exposure * self.habituation)
        trait_mod = self.personality['openness'] + 0.5*self.digital_literacy
        sentiment = nlp_result.get("sentiment", 0)
        bias = nlp_result.get("bias", 0)
        peer_factor = 1.0 + peer_influence * self.personality['agreeableness']
        group_drift = np.mean([p.ideology for p in self.social_circle]) if self.social_circle else 0
        herd_drift = (group_drift - self.ideology) * 0.2 * self.personality['agreeableness']
        alignment = 1 if (np.sign(sentiment) == np.sign(self.ideology)) else -1
        confirmation = alignment * (abs(self.ideology) + 0.1 * self.personality['conscientiousness'])
        impact = sentiment * interest_boost * habituation_factor * trait_mod * peer_factor + herd_drift
        impact *= (1 + confirmation * self.polarization)
        entrenchment = max(0, abs(self.core_beliefs) * (1 - self.personality['openness']))
        impact *= (1 - entrenchment)
        is_misinfo = nlp_result.get("subtext", "").lower().startswith("misinfo")
        if is_misinfo:
            self.misinformation_exposure += 1
            if self.misinformation_exposure > 3:
                self.trust -= 0.07 * (self.misinformation_exposure - 2) * (1-self.digital_literacy)
        else:
            self.trust += (impact / 10.0) * (self.digital_literacy+0.2)
        self.trust = np.clip(self.trust, 0, 1)
        self.ideology += impact * self.polarization * alignment
        self.ideology = np.clip(self.ideology, -1, 1)
        if abs(self.ideology) > 0.8:
            self.core_beliefs = 0.8*np.sign(self.ideology) + 0.2*self.core_beliefs
        if abs(sentiment) > 0.8:
            self.emotion = 'outraged' if sentiment < 0 else 'hopeful'
        elif abs(impact) > 0.5:
            self.emotion = 'curious'
        elif exposure > 12:
            self.emotion = 'apathetic'
        elif peer_influence > 0.2:
            self.emotion = 'anxious'
        else:
            self.emotion = 'neutral'
        self.memory.append((headline, topic, sentiment, impact, self.emotion, None))
        self.topic_exposure[topic] += 1
        self._decay_memory()
        self.log.append({
            'headline': headline, 'topic': topic, 'sentiment': sentiment,
            'ideology': self.ideology, 'trust': self.trust, 'emotion': self.emotion,
            'exposure': self.topic_exposure[topic], 'core_beliefs': self.core_beliefs,
            'misinfo': is_misinfo, 'peer_influence': peer_influence, 'traits': self.personality
        })

    def recover(self):
        self.ideology -= np.sign(self.ideology) * self.recovery
        self.ideology = np.clip(self.ideology, -1, 1)
        self.trust += (0.5 - self.trust) * self.recovery
        self.trust = np.clip(self.trust, 0, 1)
        if self.emotion in ('outraged', 'apathetic'):
            self.emotion = 'neutral'

    def auto_learn(self):
        if self.topic_exposure:
            least_seen = min(self.topic_exposure, key=self.topic_exposure.get)
            if random.random() < 0.15:
                self.ideology += random.uniform(-0.02, 0.02)
                self.emotion = 'curious'
            if self.emotion != 'neutral':
                self.recover()

    def summary(self):
        return {
            'name': self.name, 'age': self.age, 'ideology': round(self.ideology,2),
            'trust': round(self.trust,2), 'emotion': self.emotion,
            'top_interest': max(self.topic_exposure, key=self.topic_exposure.get, default=None),
            'digital_literacy': round(self.digital_literacy,2),
            'traits': {k:round(v,2) for k,v in self.personality.items()},
            'media_habits': self.media_habits
        }

    def export_log(self):
        import pandas as pd
        return pd.DataFrame(self.log)

    def explain(self):
        expl = f"{self.name} ({self.age}): Ideology={self.ideology:.2f}, Trust={self.trust:.2f}, Emotion={self.emotion}."
        expl += f" Core beliefs {self.core_beliefs:.2f}. "
        expl += f"Digital literacy: {self.digital_literacy:.2f}. Media habits: {', '.join(self.media_habits)}."
        expl += " Traits: " + ", ".join([f"{k}={v:.2f}" for k,v in self.personality.items()]) + ". "
        if self.ideology > 0.5:
            expl += "Leans right."
        elif self.ideology < -0.5:
            expl += "Leans left."
        else:
            expl += "Moderate."
        expl += f" Most engaged with {self.summary()['top_interest'] or 'no topic yet'}."
        if self.misinformation_exposure > 2:
            expl += " Is growing skeptical from repeated misinformation."
        return expl
