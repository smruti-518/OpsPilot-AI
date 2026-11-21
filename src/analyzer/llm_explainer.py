
import os
from groq import Groq


def generate_llm_explanation(incident_data, analysis):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {
            "available": False,
            "message": "Groq API key is not configured."
        }

    evidence = analysis.get("evidence", [])

    prompt = f"""
You are an experienced production support and DevOps engineer.

Analyze the following incident using only the supplied evidence.

Severity: {analysis['severity']}
Severity score: {analysis['severity_score']}/100
Total logs: {incident_data['total_logs']}
Errors: {incident_data['total_errors']}
Warnings: {incident_data['total_warnings']}

Possible causes:
{analysis['possible_causes']}

Observed evidence:
{evidence}

Business impact:
{analysis['impact_description']}

Provide:
1. Incident summary
2. Most likely technical explanation
3. Evidence supporting the explanation
4. Immediate L1 actions
5. L2 troubleshooting steps
6. Prevention recommendations

Rules:
- Do not claim the root cause is confirmed.
- Do not invent metrics or events.
- Do not suggest destructive production commands.
- Clearly distinguish facts from hypotheses.
"""

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful production incident "
                        "analysis assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_completion_tokens=1200
        )

        explanation = response.choices[0].message.content

        return {
            "available": True,
            "message": explanation
        }

    except Exception as error:
        return {
            "available": False,
            "message": f"Groq API error: {str(error)[:300]}"
        }
