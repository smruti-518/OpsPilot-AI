
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analyzer.log_parser import parse_logs
from src.analyzer.incident_detector import detect_incidents
from src.analyzer.severity_engine import classify_severity
from src.analyzer.ai_analyzer import generate_analysis
from src.analyzer.llm_explainer import generate_llm_explanation
from src.reporting.report_generator import generate_report
from src.storage.database import (
    initialize_database,
    save_incident,
    get_incident_history,
    get_incident_report
)

BASE_DIR = Path(__file__).parent
SCENARIO_DIR = BASE_DIR / "data" / "scenarios"

st.set_page_config(
    page_title="OpsPilot AI",
    page_icon="🚨",
    layout="wide"
)

initialize_database()

st.title("🚨 OpsPilot AI")
st.subheader("AI-Powered Incident Analyzer")
st.caption(
    "Operational incident intelligence | Log analysis | "
    "Severity assessment | L1/L2 investigation"
)

# INPUT
st.header("1. Choose an incident scenario")

scenarios = {
    "Default database and payment incident":
        BASE_DIR / "data" / "sample_logs.txt",
    "Database failure":
        SCENARIO_DIR / "database_failure.txt",
    "API timeout":
        SCENARIO_DIR / "api_timeout.txt",
    "CPU and memory saturation":
        SCENARIO_DIR / "resource_saturation.txt",
    "Payment gateway failure":
        SCENARIO_DIR / "payment_failure.txt",
    "Healthy application":
        SCENARIO_DIR / "healthy_application.txt",
}

selected_scenario = st.selectbox(
    "Load a demonstration scenario",
    list(scenarios.keys())
)

scenario_path = scenarios[selected_scenario]

default_logs = (
    scenario_path.read_text(encoding="utf-8")
    if scenario_path.exists()
    else ""
)

uploaded_file = st.file_uploader(
    "Or upload your own log file",
    type=["txt", "log"]
)

if uploaded_file:
    log_text = uploaded_file.getvalue().decode(
        "utf-8", errors="replace"
    )
else:
    log_text = st.text_area(
        "Application logs",
        value=default_logs,
        height=220
    )

# ANALYSIS
if st.button("Analyze Incident", type="primary"):

    if not log_text.strip():
        st.warning("Please provide application logs.")

    else:
        parsed_logs = parse_logs(log_text)

        if not parsed_logs:
            st.error("No valid log entries found.")

        else:
            with st.spinner("Analyzing logs and generating AI explanation..."):

                incident_data = detect_incidents(parsed_logs)

                severity_data = classify_severity(
                    incident_data
                )

                analysis = generate_analysis(
                    incident_data,
                    severity_data
                )

                # Generate LLM explanation
                llm_result = generate_llm_explanation(
                    incident_data,
                    analysis
                )

                # Generate report
                report = generate_report(
                    incident_data,
                    analysis
                )

                if llm_result["available"]:
                    report += (
                        "\n\nAI-POWERED INCIDENT EXPLANATION\n"
                        + "=" * 45
                        + "\n"
                        + llm_result["message"]
                    )

                else:
                    report += (
                        "\n\nAI EXPLANATION STATUS\n"
                        + llm_result["message"]
                    )

                # Save incident
                save_incident(
                    incident_data,
                    analysis,
                    report
                )

                # Preserve results across Streamlit reruns
                st.session_state["incident_data"] = incident_data
                st.session_state["analysis"] = analysis
                st.session_state["report"] = report
                st.session_state["llm_result"] = llm_result

            st.success(
                f"Incident {analysis['incident_id']} analyzed and saved."
            )

# RESULTS
if "analysis" in st.session_state:

    incident_data = st.session_state["incident_data"]
    analysis = st.session_state["analysis"]
    report = st.session_state["report"]
    llm_result = st.session_state.get(
        "llm_result",
        {"available": False, "message": "No AI explanation available."}
    )

    st.divider()
    st.header("2. Incident overview")

    st.write(f"**Incident ID:** `{analysis['incident_id']}`")
    st.write(f"**Detected:** {analysis['detected_at']}")

    severity = analysis["severity"]

    if severity == "Critical":
        st.error(f"Severity: {severity}")
    elif severity == "High":
        st.warning(f"Severity: {severity}")
    elif severity == "Medium":
        st.info(f"Severity: {severity}")
    else:
        st.success(f"Severity: {severity}")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total logs", incident_data["total_logs"])
    c2.metric("Errors", incident_data["total_errors"])
    c3.metric("Warnings", incident_data["total_warnings"])
    c4.metric("Severity score", f"{analysis['severity_score']}/100")

    st.caption(
        "Severity uses custom prototype rules, "
        "not an industry-standard metric."
    )

    # LOG ANALYSIS
    st.divider()
    st.header("3. Log analysis")

    level_counts = incident_data["level_counts"]

    if level_counts:
        chart_data = pd.DataFrame(
            list(level_counts.items()),
            columns=["Log Level", "Count"]
        )

        left, right = st.columns(2)

        with left:
            fig = px.pie(
                chart_data,
                names="Log Level",
                values="Count",
                title="Log Level Distribution",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)

        with right:
            fig = px.bar(
                chart_data,
                x="Log Level",
                y="Count",
                color="Log Level",
                text="Count",
                title="Log Count by Level"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Incident timeline")

    timeline_df = pd.DataFrame(
        incident_data["timeline"]
    )

    if not timeline_df.empty:
        st.dataframe(
            timeline_df,
            use_container_width=True,
            hide_index=True
        )

    # CORRELATIONS
    st.divider()
    st.header("4. Incident correlations")

    if analysis["correlations"]:
        for item in analysis["correlations"]:
            with st.expander(item["title"], expanded=True):
                st.write(item["explanation"])
                st.caption(item["confidence"])

                for evidence in item["evidence"]:
                    st.write(f"- {evidence}")
    else:
        st.info("No correlations detected.")

    # ROOT CAUSE HYPOTHESES
    st.divider()
    st.header("5. Ranked root-cause hypotheses")

    st.caption(
        "These are evidence-based hypotheses, not confirmed root causes."
    )

    for item in analysis["possible_causes"]:
        with st.expander(
            f"Rank {item['rank']}: {item['cause']}",
            expanded=True
        ):
            st.write(item["reason"])
            st.write(f"Evidence match: {item['confidence']}")
            st.write(f"Supporting entries: {item['evidence_count']}")

            for evidence in item["evidence"]:
                st.write(f"- {evidence}")

    # BUSINESS IMPACT
    st.divider()
    st.header("6. Business impact")

    st.write(f"**Impact area:** {analysis['impact_area']}")
    st.write(analysis["impact_description"])

    # GROQ AI EXPLANATION
    st.divider()
    st.header("7. AI-powered incident explanation")

    if llm_result["available"]:
        st.success("Live Groq LLM analysis generated")
        st.markdown(llm_result["message"])
    else:
        st.warning("AI explanation unavailable")
        st.write(llm_result["message"])

    # INVESTIGATION CHECKLIST
    st.divider()
    st.header("8. L1/L2 investigation checklist")

    st.caption(
        "These are guidance steps, not automated production actions."
    )

    for index, item in enumerate(
        analysis["investigation_steps"]
    ):
        st.checkbox(
            f"[{item['team']}] {item['action']}",
            key=f"{analysis['incident_id']}_step_{index}"
        )

    # EVIDENCE
    st.divider()
    st.header("9. Observed evidence")

    if analysis["evidence"]:
        for item in analysis["evidence"]:
            st.write(f"- {item}")
    else:
        st.info("No error or warning evidence detected.")

    # REPORT
    st.divider()
    st.header("10. Incident report")

    st.download_button(
        "Download complete incident report",
        data=report,
        file_name=f"{analysis['incident_id']}_report.txt",
        mime="text/plain"
    )

# HISTORY
st.divider()
st.header("11. Persistent incident history")

history = get_incident_history()

if history:

    history_df = pd.DataFrame(history)

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Export history as CSV",
        data=history_df.to_csv(index=False).encode("utf-8"),
        file_name="opspilot_history.csv",
        mime="text/csv"
    )

    selected_id = st.selectbox(
        "Select a previous incident",
        [item["incident_id"] for item in history]
    )

    if st.button("View saved report"):
        saved_report = get_incident_report(selected_id)

        if saved_report:
            st.text_area(
                "Previous incident report",
                saved_report,
                height=350
            )

else:
    st.info("No incidents saved yet.")

st.divider()
st.caption(
    "OpsPilot AI | Technology Operations Incident Intelligence"
)
