# app.py — Streamlit Frontend for Prometheus Simulation

import streamlit as st
from persona_engine import load_personas, run_simulation, save_state, auto_run_news_simulation

st.set_page_config(page_title="Prometheus Simulation", layout="wide")

st.title("🧠 Prometheus: Media Reaction Simulator")
st.caption("Understand how age-based personas respond to headlines")

# === Input for headline or news feed ===
mode = st.radio("Choose simulation mode:", ["Manual headline", "Live news auto-run"])

if mode == "Manual headline":
    headline = st.text_input("Enter a headline:", value="Supreme Court strikes down federal ban on bump stocks")

    if st.button("Run Simulation"):
        results = run_simulation(load_personas(), headline)
        save_state()

        st.subheader("Persona Reactions")
        for r in results:
            st.markdown(f"**🧍 {r['name']} ({r['age']})**")
            st.markdown(f"**🧭 Ideology:** `{r['reaction'].get('ideology', 'unknown')}`")
            st.markdown(f"**📊 Emotion:** `{r['reaction']['emotion']}`")
            st.markdown(f"**📉 Trust Level:** `{r['reaction']['trust_level']}`")
            st.caption(f"📝 {r['reaction']['summary']}")
            st.caption(f"📌 {r['reaction']['note']}")
            st.markdown("---")

else:
    st.warning("Running auto-news feed simulation...")
    auto_run_news_simulation()
    st.success("Auto-run complete. Persona state updated.")


