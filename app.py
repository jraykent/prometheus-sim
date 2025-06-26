import streamlit as st
import pandas as pd
import json
import io
from persona_engine import load_personas, run_simulation, save_state, auto_run_news_simulation

st.set_page_config(page_title="Prometheus Simulation", layout="centered")
st.title("🧠 Prometheus: Generational AI Persona Simulator")

# --- SIDEBAR CONTROLS FOR TWEAKING BEHAVIOR ---
st.sidebar.header("🛠️ Simulation Controls")
trust_step = st.sidebar.slider(
    "Default trust change per headline",
    min_value=-0.1, max_value=0.1, value=0.01, step=0.01
)
ideology_chance = st.sidebar.slider(
    "Chance of ideology change (%)",
    min_value=0, max_value=100, value=10, step=1
)

if st.button("📰 Auto-Run from News Feeds"):
    auto_run_news_simulation(trust_step=trust_step, ideology_chance=ideology_chance)
    st.success("News simulation run completed and saved.")

headline = st.text_input("Enter a headline to simulate reactions:")

if st.button("Run Simulation") and headline:
    results = run_simulation(load_personas(), headline, trust_step=trust_step, ideology_chance=ideology_chance)
    save_state(results)
    st.success("Simulation complete. Scroll down to see persona histories.")

personas = load_personas()

if st.button("⬇️ Download ALL Persona Logs (JSON)"):
    all_logs = {p['name']: p.get('belief_log', []) for p in personas}
    st.download_button(
        "Download All Logs as JSON",
        data=json.dumps(all_logs, indent=2),
        file_name="all_persona_logs.json",
        mime="application/json"
    )

st.header("Persona Memory Logs & Trends")

for p in personas:
    with st.expander(f"{p['name']} ({p['age']} yrs) — Ideology: {p.get('ideology', 'unknown')}"):
        st.markdown(f"**Current Trust:** `{p.get('trust', 'unknown')}`")
        st.markdown("#### Memory Timeline:")

        if p.get("belief_log"):
            mem = p["belief_log"]
            data = []
            for entry in mem:
                reaction = entry["reaction"]
                data.append({
                    "timestamp": reaction["timestamp"],
                    "trust": reaction.get("trust_level", None),
                    "ideology": reaction.get("ideology", "unknown"),
                    "emotion": reaction.get("emotion", "unknown"),
                    "headline": entry["headline"]
                })
            df = pd.DataFrame(data)
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            st.line_chart(df.set_index("timestamp")["trust"], height=150, use_container_width=True)
            st.markdown("##### Ideology History:")
            st.write(df[["timestamp", "ideology"]].tail(20))

            for entry in reversed(mem[-20:]):
                st.markdown(
                    f"**{entry['headline']}**\n\n"
                    f"— *{entry['reaction']['timestamp']}*  \n"
                    f"Emotion: `{entry['reaction']['emotion']}` | Trust: `{entry['reaction']['trust_level']}` | Ideology: `{entry['reaction'].get('ideology', 'unknown')}`\n"
                    f"> {entry['reaction']['summary']}"
                )
                st.markdown("---")

            json_data = json.dumps(mem, indent=2)
            st.download_button("⬇️ Download Memory as JSON", json_data, file_name=f"{p['name']}_memory.json", mime="application/json")

            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button("⬇️ Download Memory as CSV", csv_buffer.getvalue(), file_name=f"{p['name']}_memory.csv", mime="text/csv")

        else:
            st.caption("No memory yet. Run a simulation!")

if st.button("🔁 Reset Logs"):
    import reset_logs
    reset_logs.clear_logs()
    st.warning("Persona logs reset.")
