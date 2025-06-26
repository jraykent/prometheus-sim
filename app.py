import streamlit as st
from persona_engine import load_personas, run_simulation, save_state, auto_run_news_simulation

st.set_page_config(page_title="Prometheus Simulation", layout="centered")
st.title("🧠 Prometheus: Generational AI Persona Simulator")

if st.button("📰 Auto-Run from News Feeds"):
    auto_run_news_simulation()
    st.success("News simulation run completed and saved.")

headline = st.text_input("Enter a headline to simulate reactions:")

if st.button("Run Simulation") and headline:
    results = run_simulation(load_personas(), headline)
    save_state(results)
    st.success("Simulation complete. Scroll down to see persona histories.")

personas = load_personas()
st.header("Persona Memory Logs")
for p in personas:
    with st.expander(f"{p['name']} ({p['age']} yrs) — Ideology: {p.get('ideology', 'unknown')}"):
        st.markdown(f"**Current Trust:** `{p.get('trust', 'unknown')}`")
        st.markdown("#### Memory Timeline:")
        if p.get("belief_log"):
            for entry in reversed(p["belief_log"][-20:]):  # Last 20 entries
                st.markdown(
                    f"**{entry['headline']}**\n\n"
                    f"— *{entry['reaction']['timestamp']}*  \n"
                    f"Emotion: `{entry['reaction']['emotion']}` | Trust: `{entry['reaction']['trust_level']}` | Ideology: `{entry['reaction'].get('ideology', 'unknown')}`\n"
                    f"> {entry['reaction']['summary']}"
                )
                st.markdown("---")
        else:
            st.caption("No memory yet. Run a simulation!")

if st.button("🔁 Reset Logs"):
    import reset_logs
    reset_logs.clear_logs()
    st.warning("Persona logs reset.")
