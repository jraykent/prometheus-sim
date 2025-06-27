import streamlit as st
from persona import Persona
from analytics import summarize_all, logs_to_dataframe
from visualizations import (
    plot_ideology_drift, plot_trust, plot_emotion_distribution
)

# Dummy news generator for demo
def demo_headlines():
    return [
        ("Major earthquake strikes city", "disaster", -0.8, 0.9),
        ("School opens new playground", "school", 0.6, 0.4),
        ("Election results spark protests", "politics", -0.7, 0.7),
        ("Medical breakthrough in cancer treatment", "health", 0.85, 0.8),
        ("Celebrity wins humanitarian award", "social", 0.5, 0.3),
        ("Rumors of economic downturn", "economy", -0.6, 0.5),
        ("Community hosts festival", "community", 0.3, 0.3)
    ]

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

st.title("Prometheus: Realistic Human-Like Persona Simulation")

st.sidebar.title("Simulation Controls")
headline = st.sidebar.selectbox(
    "Choose a headline/event",
    options=[h[0] for h in demo_headlines()]
)
headline_data = next(h for h in demo_headlines() if h[0] == headline)

if st.sidebar.button("Simulate Event"):
    for persona in personas:
        persona.react(*headline_data)
        persona.recover()
    st.success("Headline/event processed for all personas.")

if st.sidebar.button("Reset (Clear Memory)"):
    st.cache_resource.clear()
    st.experimental_rerun()

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
st.markdown("**Tip:** Select a headline on the left, then run simulations. Click analytics buttons above for data and graphs.")

