import streamlit as st
import pandas as pd
import json
import io
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
st.header("Persona Memory Logs & Trends")

for p in personas:
    with st.expander(f"{p['name']} ({p['age']} yrs) — Ideology: {p.get('ideology', 'unknown')}"):
        st.markdown(f"**Current Trust:** `{p.get('trust', 'unknown')}`")
        st.markdown("#### Memory Timeline:")

        # Build DataFrame from memory for plotting
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

            # Chart trust trend
            st.line_chart(df.set_index("timestamp")["trust"], height=150, use_container_width=True)
            # Show ideology as a step (categorical)
            st.markdown("##### Ideology History:")
            st.write(df[["timestamp", "ideology"]].tail(20))

            # Show last 20 memory entries in text
            for entry in reversed(mem[-20:]):
                st.markdown(
                    f"**{entry['headline']}**\n\n"
                    f"— *{entry['reaction']['timestamp']}*  \n"
                    f"Emotion: `{entry['reaction']['emotion']}` | Trust: `{entry['reaction']['trust_level']}` | Ideology: `{entry['reaction'].get('ideology', 'unknown')}`\n"
                    f"> {entry['reaction']['summary']}"
                )
                st.markdown("---")

            # Download as JSON
            json_data = json.dumps(mem, indent=2)
            st.download_button("⬇️ Download Memory as JSON", json_data, file_name=f"{p['name']}_memory.json", mime="application/json")

            # Download as CSV
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button("⬇️ Download Memory as CSV", csv_buffer.getvalue(), file_name=f"{p['name']}_memory.csv", mime="text/csv")

        else:
            st.caption("No memory yet. Run a simulation!")

if st.button("🔁 Reset Logs"):
    import reset_logs
    reset_logs.clear_logs()
    st.warning("Persona logs reset.")
