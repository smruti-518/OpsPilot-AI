
from datetime import datetime
from uuid import uuid4


def generate_analysis(incident_data, severity_data):

    error_logs = incident_data.get("error_logs", [])
    warning_logs = incident_data.get("warning_logs", [])
    all_logs = error_logs + warning_logs

    evidence = [
        log.get("message", "")
        for log in all_logs
    ]

    incident_id = (
        "INC-"
        + datetime.now().strftime("%Y%m%d-%H%M%S")
        + "-"
        + uuid4().hex[:4].upper()
    )

    detected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Identify evidence for different incident categories
    database_evidence = [
        item for item in evidence
        if any(word in item.lower() for word in [
            "database", "connection pool", "sql connection"
        ])
    ]

    payment_evidence = [
        item for item in evidence
        if any(word in item.lower() for word in [
            "payment", "transaction", "checkout"
        ])
    ]

    api_evidence = [
        item for item in evidence
        if any(word in item.lower() for word in [
            "api", "latency", "timeout", "response time", "slow"
        ])
    ]

    resource_evidence = [
        item for item in evidence
        if any(word in item.lower() for word in [
            "cpu", "memory", "out of memory", "oom",
            "worker process terminated", "resource",
            "disk full", "disk usage", "high utilization"
        ])
    ]

    # Generate ranked root-cause hypotheses
    hypotheses = []

    if resource_evidence:
        hypotheses.append({
            "cause": "CPU and memory resource saturation",
            "reason": (
                "Resource-related indicators such as high CPU usage, "
                "high memory usage, or process termination were detected."
            ),
            "confidence": "Strong evidence match",
            "evidence_count": len(resource_evidence),
            "evidence": resource_evidence
        })

    if database_evidence:
        hypotheses.append({
            "cause": "Database connectivity or connection pool failure",
            "reason": "Database errors or connection pool indicators were detected.",
            "confidence": "Strong evidence match",
            "evidence_count": len(database_evidence),
            "evidence": database_evidence
        })

    if payment_evidence:
        hypotheses.append({
            "cause": "Payment transaction processing failure",
            "reason": "Payment or transaction-related failures were detected.",
            "confidence": "Evidence match",
            "evidence_count": len(payment_evidence),
            "evidence": payment_evidence
        })

    if api_evidence:
        hypotheses.append({
            "cause": "API performance degradation",
            "reason": "API latency or timeout indicators were detected.",
            "confidence": "Evidence match",
            "evidence_count": len(api_evidence),
            "evidence": api_evidence
        })

    hypotheses.sort(
        key=lambda item: item["evidence_count"],
        reverse=True
    )

    for index, item in enumerate(hypotheses, start=1):
        item["rank"] = index

    incident_detected = bool(error_logs or warning_logs)

    # Determine business impact
    resource_affected = bool(resource_evidence)
    payment_affected = bool(payment_evidence)
    database_affected = bool(database_evidence)
    api_affected = bool(api_evidence)

    if resource_affected:
        impact_area = "Application and infrastructure availability"
        impact_description = (
            "High CPU or memory utilization may reduce application "
            "capacity, cause worker termination, and degrade service performance."
        )

    elif payment_affected:
        impact_area = "Payment processing"
        impact_description = (
            "Payment transactions may be delayed or unsuccessful. "
            "Verify transaction status before retrying."
        )

    elif database_affected:
        impact_area = "Data access"
        impact_description = (
            "Application operations that depend on database connectivity "
            "may be delayed or unavailable."
        )

    elif api_affected:
        impact_area = "API availability and performance"
        impact_description = (
            "Users or dependent services may experience slow API responses."
        )

    elif incident_detected:
        impact_area = "Potential application impact"
        impact_description = (
            "An issue was detected, but its specific business impact "
            "could not be determined from the available log evidence."
        )

    else:
        impact_area = "Undetermined"
        impact_description = (
            "No errors or warnings were detected in the analyzed logs. "
            "The application appears healthy based on the available evidence."
        )

    # Generate L1/L2 investigation checklist
    investigation_steps = []

    if incident_detected:
        investigation_steps.extend([
            {
                "team": "L1 Support",
                "action": "Record the incident ID, detection time, and affected service."
            },
            {
                "team": "L1 Support",
                "action": "Check application health and confirm whether the issue is ongoing."
            },
            {
                "team": "L1 Support",
                "action": "Collect relevant logs and identify the first observed error."
            }
        ])

        if resource_affected:
            investigation_steps.extend([
                {
                    "team": "L2 Support",
                    "action": "Check CPU, memory, and disk utilization against configured thresholds."
                },
                {
                    "team": "L2 Support",
                    "action": "Investigate out-of-memory errors and terminated worker processes."
                },
                {
                    "team": "L2 Support",
                    "action": "Review resource limits, recent deployments, and possible memory leaks."
                }
            ])

        if database_affected:
            investigation_steps.extend([
                {
                    "team": "L2 Support",
                    "action": "Verify database server availability and connectivity."
                },
                {
                    "team": "L2 Support",
                    "action": "Inspect active database connections and connection pool usage."
                }
            ])

        if payment_affected:
            investigation_steps.extend([
                {
                    "team": "L2 Support",
                    "action": "Identify affected payment transactions and verify their final status."
                },
                {
                    "team": "L2 Support",
                    "action": "Avoid duplicate transaction retries until status is verified."
                }
            ])

        if api_affected:
            investigation_steps.append({
                "team": "L2 Support",
                "action": "Review API response times, timeout rates, and dependent services."
            })

        investigation_steps.append({
            "team": "L2 Support",
            "action": "Document findings and escalate unresolved issues."
        })

    recommendations = list(dict.fromkeys(
        item["action"] for item in investigation_steps
    ))

    return {
        "incident_id": incident_id,
        "detected_at": detected_at,
        "incident_detected": incident_detected,
        "severity": severity_data.get("severity", "Low"),
        "severity_score": severity_data.get("score", 0),
        "severity_reason": severity_data.get("reason", ""),
        "scoring_details": severity_data.get("scoring_details", []),
        "evidence": evidence,
        "possible_causes": hypotheses,
        "impact_area": impact_area,
        "impact_description": impact_description,
        "investigation_steps": investigation_steps,
        "recommendations": recommendations,
        "correlations": incident_data.get("correlations", []),
        "root_cause_confirmed": False,
        "analysis_type": "Rule-based incident intelligence"
    }
