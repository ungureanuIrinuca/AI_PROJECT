import ollama

from analize.analysis import (
    analyze_heart_rate,
    analyze_sleep,
    calculate_health_score
)


class HealthAgent:

    def __init__(self, model="mistral"):
        self.__model = model

    def analyze(self, data):

        heart_rate_analysis = analyze_heart_rate(
            [data["heart_rate"]]
        )

        sleep_analysis = analyze_sleep(
            data["sleep_hours"]
        )

        health_score_analysis = calculate_health_score(
            [data["heart_rate"]],
            data["sleep_hours"],
            data["steps"]
        )

        prompt = f"""
You are a Business Intelligence health assistant.

Heart Rate Analysis:
{heart_rate_analysis}

Sleep Analysis:
{sleep_analysis}

Health Score Analysis:
{health_score_analysis}

Generate:

1. Three business intelligence insights.
2. Three personalized recommendations.

Return EXACTLY this format:

INSIGHTS:
- insight
- insight
- insight

RECOMMENDATIONS:
- recommendation
- recommendation
- recommendation
"""

        response = ollama.chat(
            model=self.__model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        llm_response = response["message"]["content"]

        insights = []
        recommendations = []

        current_section = None

        for line in llm_response.split("\n"):

            line = line.strip()

            if not line:
                continue

            if line.upper().startswith(
                    "INSIGHTS"):
                current_section = "insights"
                continue

            if line.upper().startswith(
                    "RECOMMENDATIONS"):
                current_section = "recommendations"
                continue

            if line.startswith("-"):
                line = line[1:].strip()

            if current_section == "insights":
                insights.append(line)

            elif current_section == "recommendations":
                recommendations.append(line)

        return {

            "health_score":
                health_score_analysis[
                    "health_score"
                ],

            "health_status":
                health_score_analysis[
                    "health_status"
                ],

            "heart_rate_analysis":
                heart_rate_analysis,

            "sleep_analysis":
                sleep_analysis,

            "business_insights":
                insights[:3],

            "recommendations":
                recommendations[:3]
        }