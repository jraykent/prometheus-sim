# app.py — Prometheus Dashboard

import streamlit as st
from persona_engine import load_personas, run_simulation, save_state
import json
import os

# Page configuration
st.set_page_config(page_title="Prometheus AI Simulation", layout="centered")
st.title("🧠 Prometheus Persona Engine")
st.markdown("Enter a headline, tweet, or news summary to simulate persona reactions:")

# Headline input
headline = st.text_input("📰 Enter headline or content:")

# Run simulation on button press
if st.button("▶️ Run Simulation") and headline.strip():
    try:
        st.info("Running simulation...")
        results = run_simulation(load_personas(), headline)

        for r in results:
            st.subheader(f"{r['name']} (Age {r['age']})")
            st.markdown(f"**📝 Summary:** {r['reaction'].get('summary', 'N/A')}**")
            st.markdown(f"**😐 Emotion:** {r['reaction'].get('emotion', 'N/A')}**")
            st.markdown(f"**🔒 Trust Level:** `{r['reaction'].get('trust_level', 'unknown')}`")
            st.markdown(f"**🧭 Ideology:** `{r['reaction'].get('ideology', 'unknown')}`")
            st.caption(f"📌 {r['reaction'].get('note', '')}")
            st.markdown("---")

    except Exception as e:
        st.error(f"⚠️ An error occurred during simulation: {e}")

# Optional: Save the updated belief states
if st.button("💾 Save Persona State"):
    try:
        save_state()
        st.success("✅ Persona states saved to logs/personas_state.json")
    except Exception as e:
        st.error(f"⚠️ Failed to save states: {e}")


