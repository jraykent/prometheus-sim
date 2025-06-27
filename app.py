import streamlit as st
from persona import Persona
from news_ingest import get_sample_headlines, fetch_newsapi_headlines, fetch_reddit_headlines
from simulation import run_simulation, run_blackbox
from analytics import summarize_all, logs_to_dataframe
from visualizations import plot_ideology_drift, plot_trust, plot_emotion_distribution
from export_utils import export_persona_logs
import random

@st.cache_resource
def create_personas():
    return [
        Persona("Lily", 8),
        Persona("Jordan", 16),
        Persona("Alex", 34),
        Persona("Pat", 52),
        Persona("Morgan", 70)
    ]

personas = create_personas()

st.title("Prometheus: Generational AI Influence Simulation")

# -- Headline source selection --
st.sidebar.title("Headline Sources")
headline_mode = st.sidebar.radio("Select source", ["Sample Demo", "NewsAPI", "Reddit"])
if headline_mode == "Sample Demo":
    headlines = get_sample_headlines()
elif headline_mode == "NewsAPI":
    headlines = fetch_newsapi_headlines() or get_sample_headlines()
else:
    headlines = fetch_reddit_headlines() or get_sample_headlines()

headline = st.sidebar.selectbox(
    "Choose a headline/event",
    options=[h[0] for h in headlines]
)
headline_data = next(h for h in headlines if h[0] == headline)

if st.sidebar.button("Simulate Event"):
    peer_ideologies = [p.ideology for p in personas]
    for idx, persona in enumerate(personas):
        peer_mean = sum(peer_ideologies)/len(peer_ideologies)
        peer_influence = (peer_mean - persona.ideology) * 0.2
        persona.react(*headline_data, peer_influence=peer_influence)
        persona.recover()
    st.success("Headline/event processed for all personas.")

if st.sidebar.button("Run Auto Simulation (10 steps)"):
    run_simulation(personas, headlines, steps=10)
    st.success("Auto simulation (10 steps) complete.")

if st.sidebar.button("Black Box Mode (adversarial, 10 steps)"):
    adversarial_headlines = [
        ("Fake scandal rocks nation", "politics", -0.95, 0.95),
        ("Viral conspiracy shocks youth", "social", -0.85, 0.88),
        ("Health crisis blamed on tech", "health", -0.9, 0.85)
    ]
    run_blackbox(personas, adversarial_headlines, steps=10)
    st.success("Black box run complete.")

if st.sidebar.button("Reset (Clear Memory)"):
    st.cache_resource.clear()
    st.experimental_rerun()

# -- Analytics & Visualization --
if st.button("Show Persona Summaries"):
    st.dataframe(summarize_all(personas))

if st.button("Show Raw Persona Logs Table"):
    df = logs_to_dataframe(personas)
    st.dataframe(df)

if st.button("Visualize Ideology Drift"):
    fig = plot_ideology_drift(personas)
    st.pyplot(fig)

if st.button("Visualize Trust Levels"):
    fig = plot_trust(personas)
    st.pyplot(fig)

if st.button("Show Emotion Distribution"):
    fig = plot_emotion_distribution(personas)
    st.pyplot(fig)

if st.button("Explain Personas"):
    for p in personas:
        st.write(p.explain())

st.markdown("---")
st.markdown("**Tip:** Use the sidebar for source/news selection and simulation. Use analytics buttons above to explore results and trends.")

