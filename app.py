import streamlit as st
from persona import Persona
from news_ingest import get_sample_headlines, fetch_newsapi_headlines, generate_synthetic_headline
from simulation import run_simulation, run_blackbox
from analytics import summarize_all, compute_drift
from visualizations import plot_ideology_drift, plot_emotion_distribution
from export_utils import export_persona_logs

@st.cache_resource
def create_personas():
    return [
        Persona("Sam", 8),
        Persona("Alex", 16),
        Persona("Jamie", 28),
        Persona("Morgan", 45),
        Persona("Pat", 68)
    ]

personas = create_personas()

st.title("Prometheus: Generational AI Influence Simulation")

headline_mode = st.radio("Headline Source", ["Demo Headlines", "NewsAPI", "Synthetic"])
if headline_mode == "Demo Headlines":
    headlines = get_sample_headlines()
elif headline_mode == "NewsAPI":
    headlines = fetch_newsapi_headlines() or get_sample_headlines()
else:
    headlines = [generate_synthetic_headline() for _ in range(5)]

headline = st.selectbox("Choose a headline", [h[0] for h in headlines])
headline_data = next(h for h in headlines if h[0] == headline)

if st.button("Step: Simulate One Event"):
    for persona in personas:
        persona.react(*headline_data)
        persona.auto_learn()
    st.success("Event processed.")

if st.button("Run Auto Simulation (10 steps)"):
    run_simulation(personas, headlines, steps=10)
    st.success("Auto-run complete.")

if st.button("Black Box Mode (adversarial, 10 steps)"):
    adversarial_headlines = [
        ("Fake scandal rocks nation", "politics", -0.95),
        ("Viral conspiracy shocks youth", "social", -0.85),
        ("Health crisis blamed on tech", "health", -0.9)
    ]
    run_blackbox(personas, adversarial_headlines, steps=10)
    st.success("Black box run complete.")

if st.button("Show Persona Summaries"):
    st.dataframe(summarize_all(personas))

if st.button("Visualize Ideology Drift"):
    fig = plot_ideology_drift(personas)
    st.pyplot(fig)

if st.button("Show Emotion Distribution"):
    fig = plot_emotion_distribution(personas)
    st.pyplot(fig)

if st.button("Export All Logs (CSV)"):
    csv = export_persona_logs(personas, "csv")
    st.download_button("Download CSV", csv, "persona_logs.csv")

if st.button("Explain Personas"):
    for p in personas:
        st.write(p.explain())
