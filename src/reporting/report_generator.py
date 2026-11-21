
from datetime import datetime


def generate_report(incident_data, analysis):
    lines = [
        "OPSPILOT AI - INCIDENT REPORT",
        "=" * 55,
        f"Incident ID: {analysis['incident_id']}",
        f"Detected at: {analysis['detected_at']}",
        f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "INCIDENT SUMMARY",
        "-" * 35,
        f"Severity: {analysis['severity']}",
        f"Severity score: {analysis['severity_score']}/100",
        f"Total logs: {incident_data['total_logs']}",
        f"Errors: {incident_data['total_errors']}",
        f"Warnings: {incident_data['total_warnings']}",
        f"Analysis method: {analysis['analysis_type']}",
        "",
        "BUSINESS IMPACT",
        "-" * 35,
        f"Impact area: {analysis['impact_area']}",
        analysis["impact_description"],
        "",
        "SEVERITY REASON",
        "-" * 35,
        analysis["severity_reason"],
        "",
        "OBSERVED EVIDENCE",
        "-" * 35
    ]

    for item in analysis["evidence"]:
        lines.append(f"- {item}")

    lines.extend([
        "",
        "RANKED ROOT-CAUSE HYPOTHESES",
        "-" * 35
    ])

    for cause in analysis["possible_causes"]:
        lines.extend([
            f"\nRank {cause['rank']}: {cause['cause']}",
            f"Reason: {cause['reason']}",
            f"Evidence match: {cause['confidence']}",
            f"Supporting log entries: {cause['evidence_count']}"
        ])

        for item in cause["evidence"]:
            lines.append(f"  - {item}")

    lines.extend([
        "",
        "INCIDENT CORRELATIONS",
        "-" * 35
    ])

    if analysis["correlations"]:
        for item in analysis["correlations"]:
            lines.append(f"- {item['title']}")
            lines.append(f"  {item['explanation']}")
    else:
        lines.append("No correlations detected.")

    lines.extend([
        "",
        "L1/L2 INVESTIGATION CHECKLIST",
        "-" * 35
    ])

    for index, step in enumerate(
        analysis["investigation_steps"], start=1
    ):
        lines.append(
            f"{index}. [{step['team']}] {step['action']}"
        )

    lines.extend([
        "",
        f"Root cause confirmed: {analysis['root_cause_confirmed']}",
        "",
        "Note: This report contains rule-based hypotheses. "
        "Validate findings before taking production action.",
        "END OF REPORT"
    ])

    return "\n".join(lines)
