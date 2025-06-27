import streamlit as st
from persona import Persona
from news_ingest import get_all_headlines
from simulation import run_simulation, run_blackbox
from analytics import summarize_all, logs_to_dataframe, compute_polarization
from visualizations import (
    plot_ideology_drift,
    plot_ideology_histogram,
    plot_trust,
    plot_emotion_distribution
)
from export_utils import export_persona_logs
from admin_toolkit import admin_panel
import random
import schedule
import time

st.set_page_config(page_title="Prometheus Simulation", layout="wide")

# --- Persona Creation ---
@st.cache_resource
def create_personas():
    demo_personas = [
        Persona("Lily", 8, region="West", education="Elementary"),
        Persona("Jordan", 16, region="Midwest", education="High School"),
        Persona("Alex", 34, region="South", education="Bachelor"),
        Persona("Pat", 52, region="Northeast", education="Master"),
        Persona("Morgan", 70, region="Midwest", education="PhD"),
    ]
    return demo_personas

personas = create_personas()

# --- Sidebar Source Selection ---
st.sidebar.title("Headline Source & Simulation Controls")
selected_sources = st.sidebar.multiselect(
    "Select data sources:",
    ["newsapi", "reddit", "twitter", "tiktok", "demo"],
    default=["newsapi", "reddit", "demo"]
)
topic = st.sidebar.text_input("Topic/query:", value="news")
num_results = st.sidebar.slider("Max per source:", 5, 20, 10)
headlines = get_all_headlines(
    sources=selected_sources,
    topic=topic,
    max_results=num_results
)

headline = st.sidebar.selectbox(
    "Choose a headline/event",
    options=[h[0] for h in headlines]
)
headline_data = next(h for h in headlines if h[0] == headline)

if st.sidebar.button("Simulate Event"):
    peer_ideologies = [p.ideology for p in personas]
    for idx, persona in enumerate(personas):
        peer_mean = sum(peer_ideologies) / len(peer_ideologies)
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

# --- Autonomous Scheduling (runs a sim cycle every N minutes) ---
def scheduled_run():
    run_simulation(personas, headlines, steps=1)

if st.sidebar.checkbox("Enable Autonomous Mode (sim every 10 min)"):
    st.info("Autonomous mode ON: Prometheus will run a step every 10 minutes (while app is open).")
    schedule.every(10).minutes.do(scheduled_run)
    while True:
        schedule.run_pending()
        time.sleep(1)

# --- Analytics & Visualization ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Show Persona Summaries"):
        st.dataframe(summarize_all(personas))

    if st.button("Export Logs (CSV)"):
        csv = export_persona_logs(personas, format="csv")
        st.download_button("Download CSV", csv, "persona_logs.csv")

with col2:
    if st.button("Show Raw Persona Logs Table"):
        df = logs_to_dataframe(personas)
        st.dataframe(df)

    if st.button("Show Political Spectrum Histogram"):
        fig = plot_ideology_histogram(personas)
        st.pyplot(fig)

with col3:
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
admin_panel(personas)
st.markdown("**Tip:** Use the sidebar for live news/social source selection and simulation. Use analytics above to explore results. The Admin Toolkit is for advanced research/management.")

