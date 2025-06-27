import streamlit as st

def log_browser(personas):
    st.subheader("Log Browser")
    for p in personas:
        st.markdown(f"**{p.name} (age {p.age}) — {p.region}, {p.education}**")
        df = p.export_log()
        st.dataframe(df)

def persona_editor(personas):
    st.subheader("Persona Editor (Prototype)")
    persona_names = [p.name for p in personas]
    selected = st.selectbox("Edit Persona", persona_names)
    persona = next(p for p in personas if p.name == selected)
    new_age = st.slider("Age", 5, 85, persona.age)
    new_region = st.text_input("Region", value=persona.region)
    new_education = st.text_input("Education", value=persona.education)
    if st.button("Apply Changes"):
        persona.age = new_age
        persona.region = new_region
        persona.education = new_education
        st.success("Persona updated!")

def admin_panel(personas):
    st.sidebar.title("Admin Toolkit")
    tool = st.sidebar.radio("Toolkit", ["Log Browser", "Persona Editor"])
    if tool == "Log Browser":
        log_browser(personas)
    elif tool == "Persona Editor":
        persona_editor(personas)
