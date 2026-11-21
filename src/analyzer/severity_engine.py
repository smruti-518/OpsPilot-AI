
def classify_severity(incident_data):
    errors = incident_data["total_errors"]
    warnings = incident_data["total_warnings"]
    repeated = incident_data["repeated_errors"]

    error_logs = incident_data.get("error_logs", [])
    warning_logs = incident_data.get("warning_logs", [])

    error_messages = " ".join(
        log["message"].lower()
        for log in error_logs
    )

    all_messages = " ".join(
        log["message"].lower()
        for log in error_logs + warning_logs
    )

    score = 0
    reasons = []

    # Error volume
    if errors >= 10:
        score += 40
        reasons.append("Very high error volume")
    elif errors >= 5:
        score += 25
        reasons.append("High error volume")
    elif errors >= 1:
        score += 10
        reasons.append("Application errors detected")

    # Repeated errors
    if repeated:
        score += 15
        reasons.append("Repeated errors detected")

    # Critical application failures
    if any(word in error_messages for word in [
        "database unavailable",
        "system crash",
        "service down",
        "outage",
        "critical failure"
    ]):
        score += 40
        reasons.append("Critical failure indicator detected")

    # High-impact failures
    if any(word in error_messages for word in [
        "database connection failed",
        "payment transaction failed",
        "connection timeout",
        "api request timeout"
    ]):
        score += 20
        reasons.append("High-impact failure detected")

    # Resource saturation indicators
    resource_failure = any(word in all_messages for word in [
        "out of memory",
        "oom",
        "worker process terminated",
        "resource exhaustion"
    ])

    resource_pressure = any(word in all_messages for word in [
        "cpu utilization",
        "memory utilization",
        "high cpu",
        "high memory",
        "disk full",
        "disk usage"
    ])

    if resource_failure:
        score += 25
        reasons.append("Resource exhaustion or process termination detected")

    if resource_pressure:
        score += 15
        reasons.append("High infrastructure resource utilization detected")

    # Warning volume
    if warnings >= 5:
        score += 15
        reasons.append("Very high warning volume")
    elif warnings >= 3:
        score += 10
        reasons.append("Multiple warnings detected")

    # Keep score within 0-100
    score = min(score, 100)

    # Severity classification
    if score >= 70:
        severity = "Critical"
    elif score >= 45:
        severity = "High"
    elif score >= 20:
        severity = "Medium"
    else:
        severity = "Low"

    return {
        "severity": severity,
        "score": score,
        "reason": (
            ", ".join(reasons)
            if reasons
            else "No significant issues detected"
        ),
        "scoring_details": reasons
    }
