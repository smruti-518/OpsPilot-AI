# OpsPilot AI – AI-Powered Incident Analyzer

**Operational Incident Intelligence | Log Analysis | Severity Assessment | L1/L2 Investigation**

OpsPilot AI is a Python-based incident analysis prototype designed to help technology operations and support teams investigate application issues using log data.

It analyzes application logs, identifies errors and warnings, assigns a prototype severity score, detects related events, and ranks possible root-cause hypotheses. It also uses the Groq Large Language Model (LLM) to generate incident explanations and troubleshooting recommendations.

## Key Features

- **Log Analysis:** Upload or paste application logs for analysis.
- **Demonstration Scenarios:** Test the application using built-in scenarios such as API timeout, database failure, payment failure, resource saturation, and healthy application.
- **Severity Assessment:** Calculate incident severity using custom rule-based scoring.
- **Incident Correlation:** Identify related warning and error events.
- **Root-Cause Hypotheses:** Rank possible causes based on supporting log evidence.
- **AI-Powered Explanation:** Generate incident summaries and troubleshooting guidance using Groq LLM.
- **L1/L2 Investigation:** Provide first-level and second-level support recommendations.
- **Business Impact Assessment:** Highlight potentially affected application services and operations.
- **Incident Reporting:** Generate incident reports.
- **Persistent Incident History:** Store analyzed incidents locally using SQLite.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| User Interface | Streamlit |
| Log Processing | Python |
| Incident Detection | Rule-based analysis |
| Severity Assessment | Custom Python rules |
| AI Explanation | Groq API |
| Database | SQLite |
| Testing | Pytest |
| Version Control | Git and GitHub |

## Project Structure

```text
OpsPilot-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── sample_logs.txt
│   └── scenarios/
│       ├── database_failure.txt
│       ├── api_timeout.txt
│       ├── resource_saturation.txt
│       ├── payment_failure.txt
│       └── healthy_application.txt
│
├── src/
│   ├── __init__.py
│   ├── analyzer/
│   │   ├── __init__.py
│   │   ├── log_parser.py
│   │   ├── incident_detector.py
│   │   ├── severity_engine.py
│   │   ├── ai_analyzer.py
│   │   └── llm_explainer.py
│   │
│   ├── reporting/
│   │   └── report_generator.py
│   │
│   └── storage/
│       └── database.py
│
└── tests/
    └── test_ops_pilot.py
```

*Note: The structure above describes the main project components. Additional modules may be present in the repository.*

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/smruti-518/OpsPilot-AI.git
cd OpsPilot-AI
```



### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure the Groq API key

Create a Groq API key through the Groq developer platform.

Set it as an environment variable in PowerShell:

```powershell
$env:GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

Do not hardcode API keys in source code or commit them to GitHub.

The application can use its rule-based analysis functionality without the Groq API key, but AI-generated explanations require a valid API key.

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your default browser.

## Running Tests

Run the automated test suite using:

```bash
python -m pytest -q
```

The project test suite currently passes all 11 tests.

## How to Use

1. Start the Streamlit application.
2. Select a built-in incident scenario or upload a `.txt` or `.log` file.
3. Review the application logs.
4. Run the incident analysis.
5. Examine the incident overview and severity score.
6. Review the incident timeline and detected correlations.
7. Inspect ranked root-cause hypotheses and supporting evidence.
8. Review the AI-generated incident explanation and L1/L2 investigation checklist.
9. Generate or download the incident report.
10. Review previously analyzed incidents in persistent incident history.

## Incident Analysis Workflow

```text
Application Logs
       |
       v
    Log Parser
       |
       v
 Incident Detection
       |
       v
 Severity Assessment
       |
       v
 Correlation and Evidence Analysis
       |
       v
 Ranked Root-Cause Hypotheses
       |
       v
 Groq LLM Explanation
       |
       v
 L1/L2 Investigation Guidance
       |
       v
 Incident Report and SQLite History
```

## Design Considerations and Limitations

- Incident detection, severity scoring, and hypothesis ranking are primarily rule-based.
- The severity score is a custom prototype metric and is not an industry-standard severity classification.
- Root-cause results are evidence-based hypotheses, not confirmed diagnoses.
- Groq LLM generates explanatory summaries and investigation recommendations from the available analysis.
- AI-generated recommendations should be reviewed by an authorized support or operations engineer before implementation.
- The prototype does not automatically modify or remediate production infrastructure.
- Incident history is stored locally using SQLite.

## Future Enhancements

- Integration with monitoring and observability platforms.
- Real-time log streaming and incident detection.
- Advanced anomaly detection using machine learning.
- Integration with cloud infrastructure and DevOps tools.
- Distributed tracing and service dependency analysis.
- Role-based access control and centralized incident management.
- Automated alerting and incident notifications.

## Disclaimer

OpsPilot AI is an educational and demonstration prototype developed to explore AI-assisted technology operations and incident investigation. It is not intended to replace production monitoring systems, established incident management processes, or human verification.

---

**Developed as a Technology Operations case study.**