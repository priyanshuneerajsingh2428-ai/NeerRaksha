import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NeerRaksha | Community Health", page_icon="💧", layout="wide")
st.title("💧 NeerRaksha")
st.subheader("Community health monitoring & early-warning prototype")
st.warning("Research demonstration only. Scores are heuristic indicators, not diagnoses or validated outbreak predictions.")

try:
    summary_response = requests.get("http://127.0.0.1:8000/api/summary", timeout=5)
    summary_response.raise_for_status()
    summary = summary_response.json()
    reports_response = requests.get("http://127.0.0.1:8000/api/reports", timeout=5)
    reports_response.raise_for_status()
    reports = reports_response.json()["reports"]
    water_response = requests.get("http://127.0.0.1:8000/api/water-observations", timeout=5)
    water_response.raise_for_status()
    water_observations = water_response.json()["water_observations"]
except requests.RequestException as exc:
    st.error(f"Could not load dashboard data from the NeerRaksha API: {exc}")
    st.stop()

rows = summary["risk_by_village"]
c1, c2, c3 = st.columns(3)
c1.metric("Villages monitored (demo)", summary["village_count"])
c2.metric("Symptom reports", len(reports))
c3.metric("Water observations", len(water_observations))

if rows:
    df = pd.DataFrame(rows)
    st.subheader("Village-level review queue")
    st.dataframe(df[["village", "score", "level", "report_count_7d", "reported_cases_7d"]], use_container_width=True)
    details_by_village = {row["village"]: row for row in rows}
    selected = st.selectbox("Inspect village", sorted(details_by_village))
    detail = details_by_village[selected]
    st.metric("Demonstration risk index", f'{detail["score"]}/100', detail["level"])
    st.write("**Review factors**")
    for factor in detail["factors"]:
        st.write(f"- {factor}")
    st.info(detail["disclaimer"])
else:
    st.info("No records available.")

st.subheader("Recent symptom reports")
st.dataframe(pd.DataFrame(reports), use_container_width=True)
st.subheader("Water observations")
st.dataframe(pd.DataFrame(water_observations), use_container_width=True)
st.caption("Demo records are synthetic. Do not enter identifiable patient information.")
