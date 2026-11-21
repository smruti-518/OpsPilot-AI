
from collections import Counter


def detect_incidents(parsed_logs):
    level_counts = Counter(
        log["level"] for log in parsed_logs
    )

    error_logs = [
        log for log in parsed_logs
        if log["level"] in ["ERROR", "CRITICAL"]
    ]

    warning_logs = [
        log for log in parsed_logs
        if log["level"] in ["WARNING", "WARN"]
    ]

    error_counts = Counter(
        log["message"] for log in error_logs
    )

    repeated_errors = {
        message: count
        for message, count in error_counts.items()
        if count > 1
    }

    correlations = []

    # Only use error and warning messages for failure correlations.
    problem_logs = error_logs + warning_logs

    problem_messages = [
        log["message"].lower()
        for log in problem_logs
    ]

    database_logs = [
        log for log in problem_logs
        if any(word in log["message"].lower()
               for word in [
                   "database",
                   "connection pool",
                   "db connection"
               ])
    ]

    payment_logs = [
        log for log in problem_logs
        if any(word in log["message"].lower()
               for word in [
                   "payment",
                   "transaction",
                   "gateway"
               ])
    ]

    api_logs = [
        log for log in problem_logs
        if any(word in log["message"].lower()
               for word in [
                   "api",
                   "latency",
                   "response time",
                   "timeout"
               ])
    ]

    # Database and payment correlation
    if database_logs and payment_logs:
        evidence = list(dict.fromkeys(
            log["message"]
            for log in database_logs + payment_logs
        ))

        correlations.append({
            "title": "Database and payment failures",
            "explanation": (
                "Database-related and payment-related warnings "
                "or errors appear together. A database issue "
                "may be contributing to payment failures."
            ),
            "confidence": "Possible relationship",
            "evidence": evidence
        })

    # API degradation correlation
    if api_logs:
        evidence = list(dict.fromkeys(
            log["message"] for log in api_logs
        ))

        correlations.append({
            "title": "API performance degradation",
            "explanation": (
                "Warning or error logs indicate API latency, "
                "timeouts, or request failures."
            ),
            "confidence": "Possible relationship",
            "evidence": evidence
        })

    # Build incident timeline
    timeline = []

    for log in parsed_logs:
        if log["level"] in ["ERROR", "CRITICAL"]:
            event_type = "Error"
        elif log["level"] in ["WARNING", "WARN"]:
            event_type = "Warning"
        else:
            event_type = "Information"

        timeline.append({
            "timestamp": log["timestamp"],
            "level": log["level"],
            "event_type": event_type,
            "event": log["message"]
        })

    return {
        "total_logs": len(parsed_logs),
        "total_errors": len(error_logs),
        "total_warnings": len(warning_logs),
        "level_counts": dict(level_counts),
        "error_logs": error_logs,
        "warning_logs": warning_logs,
        "repeated_errors": repeated_errors,
        "correlations": correlations,
        "timeline": timeline
    }

