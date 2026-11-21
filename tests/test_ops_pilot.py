
from src.analyzer.log_parser import parse_logs
from src.analyzer.incident_detector import detect_incidents
from src.analyzer.severity_engine import classify_severity
from src.analyzer.ai_analyzer import generate_analysis


SAMPLE_LOGS = """
2026-11-19 10:15:01 INFO Application started successfully
2026-11-19 10:15:02 INFO Payment service initialized
2026-11-19 10:15:03 WARNING Payment API response time is high
2026-11-19 10:15:04 ERROR Database connection failed
2026-11-19 10:15:05 ERROR Database connection failed
2026-11-19 10:15:06 WARNING Connection pool usage is high
2026-11-19 10:15:07 ERROR Payment transaction failed
2026-11-19 10:15:08 INFO Health check completed
"""


def analyze_logs(log_text):
    parsed = parse_logs(log_text)
    incidents = detect_incidents(parsed)
    severity = classify_severity(incidents)
    analysis = generate_analysis(incidents, severity)

    return parsed, incidents, severity, analysis


def test_log_parser():
    parsed = parse_logs(SAMPLE_LOGS)

    assert len(parsed) == 8
    assert parsed[0]["level"] == "INFO"
    assert parsed[3]["level"] == "ERROR"


def test_error_and_warning_detection():
    _, incidents, _, _ = analyze_logs(SAMPLE_LOGS)

    assert incidents["total_errors"] == 3
    assert incidents["total_warnings"] == 2


def test_repeated_error_detection():
    _, incidents, _, _ = analyze_logs(SAMPLE_LOGS)

    assert incidents["repeated_errors"] == {
        "Database connection failed": 2
    }


def test_severity_classification():
    _, _, severity, _ = analyze_logs(SAMPLE_LOGS)

    assert severity["severity"] == "High"
    assert severity["score"] == 45


def test_incident_correlations():
    _, incidents, _, _ = analyze_logs(SAMPLE_LOGS)

    titles = [
        item["title"]
        for item in incidents["correlations"]
    ]

    assert "Database and payment failures" in titles
    assert "API performance degradation" in titles


def test_incident_id_is_generated():
    _, _, severity, analysis = analyze_logs(SAMPLE_LOGS)

    assert analysis["incident_id"].startswith("INC-")
    assert len(analysis["incident_id"]) > 10


def test_database_is_ranked_first():
    _, _, _, analysis = analyze_logs(SAMPLE_LOGS)

    assert (
        analysis["possible_causes"][0]["cause"]
        == "Database connectivity or connection pool failure"
    )


def test_payment_business_impact():
    _, _, _, analysis = analyze_logs(SAMPLE_LOGS)

    assert analysis["impact_area"] == "Payment processing"


def test_investigation_checklist():
    _, _, _, analysis = analyze_logs(SAMPLE_LOGS)

    teams = {
        item["team"]
        for item in analysis["investigation_steps"]
    }

    assert "L1 Support" in teams
    assert "L2 Support" in teams


def test_empty_logs():
    parsed = parse_logs("")

    assert parsed == []


def test_unknown_incident():
    logs = """
2026-11-19 10:20:01 INFO Application started
2026-11-19 10:20:02 INFO Health check completed
"""

    _, incidents, severity, analysis = analyze_logs(logs)

    assert incidents["total_errors"] == 0
    assert severity["severity"] == "Low"
    assert analysis["impact_area"] == "Undetermined"
    assert analysis["root_cause_confirmed"] is False
