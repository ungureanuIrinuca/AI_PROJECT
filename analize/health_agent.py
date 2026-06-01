import json
import ollama

from analize.analysis import (
    analyze_heart_rate,
    analyze_sleep,
    calculate_health_score
)
from analize.trend_analysis import generate_health_insights
from analize.report_generator import generate_weekly_report


TOOLS = [
    {
        "name": "analyze_heart_rate",
        "description": "Analyzes heart rate values and returns average, min, max and condition (low/normal/high).",
        "parameters": {
            "type": "object",
            "properties": {
                "heart_rate_data": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "List of heart rate values in BPM"
                }
            },
            "required": ["heart_rate_data"]
        }
    },
    {
        "name": "analyze_sleep",
        "description": "Analyzes sleep duration and returns quality score and classification.",
        "parameters": {
            "type": "object",
            "properties": {
                "hours_slept": {
                    "type": "number",
                    "description": "Number of hours slept"
                }
            },
            "required": ["hours_slept"]
        }
    },
    {
        "name": "calculate_health_score",
        "description": "Calculates an overall health score based on heart rate, sleep, and steps.",
        "parameters": {
            "type": "object",
            "properties": {
                "heart_rate_data": {
                    "type": "array",
                    "items": {"type": "number"}
                },
                "hours_slept": {"type": "number"},
                "steps": {"type": "integer"}
            },
            "required": ["heart_rate_data", "hours_slept", "steps"]
        }
    },
    {
        "name": "generate_health_insights",
        "description": "Generates trend insights from historical steps and sleep data.",
        "parameters": {
            "type": "object",
            "properties": {
                "steps_history": {
                    "type": "array",
                    "items": {"type": "number"}
                },
                "sleep_history": {
                    "type": "array",
                    "items": {"type": "number"}
                }
            },
            "required": ["steps_history", "sleep_history"]
        }
    }
]

TOOL_MAP = {
    "analyze_heart_rate": lambda args: analyze_heart_rate(args["heart_rate_data"]),
    "analyze_sleep": lambda args: analyze_sleep(args["hours_slept"]),
    "calculate_health_score": lambda args: calculate_health_score(
        args["heart_rate_data"], args["hours_slept"], args["steps"]
    ),
    "generate_health_insights": lambda args: generate_health_insights(
        args["steps_history"], args["sleep_history"]
    )
}


class HealthAgent:

    def __init__(self, model="mistral"):
        self.__model = model

    def _run_tool(self, tool_name, tool_args):
        if tool_name in TOOL_MAP:
            return TOOL_MAP[tool_name](tool_args)
        return {"status": "error", "message": f"Unknown tool: {tool_name}"}

    def analyze(self, data):
        """
        Analizeaza datele de sanatate folosind:
        1. Tool calls locale pentru calcule
        2. LLM pentru interpretare si recomandari (prompt chaining)
        """

        heart_rate_analysis = self._run_tool(
            "analyze_heart_rate",
            {"heart_rate_data": [data["heart_rate"]]}
        )

        sleep_analysis = self._run_tool(
            "analyze_sleep",
            {"hours_slept": data["sleep_hours"]}
        )

        health_score_result = self._run_tool(
            "calculate_health_score",
            {
                "heart_rate_data": [data["heart_rate"]],
                "hours_slept": data["sleep_hours"],
                "steps": data.get("steps", 0)
            }
        )

        step1_summary = f"""
Heart Rate: {heart_rate_analysis.get('average_heart_rate', data['heart_rate'])} BPM — {heart_rate_analysis.get('condition', 'unknown')}
Sleep: {data['sleep_hours']} hours — quality: {sleep_analysis.get('sleep_quality', 'unknown')} (score: {sleep_analysis.get('sleep_score', 0)})
Steps: {data.get('steps', 0)} steps
Calories: {data.get('calories', 0)} kcal
Overall Health Score: {health_score_result.get('health_score', 'N/A')} / 100 — {health_score_result.get('health_status', 'unknown')}
"""

        insights_prompt = f"""You are a Business Intelligence health assistant analyzing wearable device data.

CURRENT HEALTH DATA SUMMARY:
{step1_summary}

STEP 1 — Generate exactly 3 business intelligence insights based on the data above.
Each insight should be factual and data-driven.
Format:
INSIGHTS:
- insight 1
- insight 2
- insight 3"""

        insights_response = ollama.chat(
            model=self.__model,
            messages=[{"role": "user", "content": insights_prompt}]
        )

        llm_insights_text = insights_response["message"]["content"]

        recommendations_prompt = f"""You are a health coach AI agent.

PATIENT DATA SUMMARY:
{step1_summary}

BUSINESS INSIGHTS ALREADY GENERATED:
{llm_insights_text}

STEP 2 — Based on the data and insights above, generate exactly 3 personalized, actionable recommendations.
Format:
RECOMMENDATIONS:
- recommendation 1
- recommendation 2
- recommendation 3"""

        recommendations_response = ollama.chat(
            model=self.__model,
            messages=[
                {"role": "user", "content": insights_prompt},
                {"role": "assistant", "content": llm_insights_text},
                {"role": "user", "content": recommendations_prompt}
            ]
        )

        llm_recommendations_text = recommendations_response["message"]["content"]

        insights = self._parse_section(llm_insights_text, "INSIGHTS")
        recommendations = self._parse_section(llm_recommendations_text, "RECOMMENDATIONS")

        return {
            "health_score": health_score_result.get("health_score"),
            "health_status": health_score_result.get("health_status"),
            "heart_rate_analysis": heart_rate_analysis,
            "sleep_analysis": sleep_analysis,
            "business_insights": insights[:3],
            "recommendations": recommendations[:3]
        }

    def process_request(self, user_prompt, user_data):
        """
        Interpreteaza cererea utilizatorului si apeleaza tool-ul potrivit.
        """

        greetings = [
            "hi",
            "hello",
            "hey",
            "hei",
            "salut"
        ]

        if user_prompt.lower().strip() in greetings:
            return {
                "user_request": user_prompt,
                "tool_used": "none",
                "tool_result": {},
                "agent_response":
                    "Hello! I can analyze your heart rate, sleep, steps and health trends."
            }

        prompt = user_prompt.lower()

        if "heart" in prompt or "bpm" in prompt:
            tool_result = self._run_tool(
                "analyze_heart_rate",
                {
                    "heart_rate_data": [
                        user_data.get("heart_rate", 70)
                    ]
                }
            )
            tool_name = "analyze_heart_rate"

        elif "sleep" in prompt:
            tool_result = self._run_tool(
                "analyze_sleep",
                {
                    "hours_slept":
                        user_data.get("sleep_hours", 8)
                }
            )
            tool_name = "analyze_sleep"

        elif (
                "score" in prompt
                or "health" in prompt
                or "status" in prompt
        ):
            tool_result = self._run_tool(
                "calculate_health_score",
                {
                    "heart_rate_data":
                        [user_data.get("heart_rate", 70)],
                    "hours_slept":
                        user_data.get("sleep_hours", 8),
                    "steps":
                        user_data.get("steps", 0)
                }
            )
            tool_name = "calculate_health_score"

        else:
            tool_result = {
                "status": "info",
                "message": "General health question"
            }
            tool_name = "none"

        synthesis_prompt = f"""
    You are a health assistant.

    User question:
    {user_prompt}

    Health data:
    {json.dumps(user_data)}

    Tool result:
    {json.dumps(tool_result)}

    Provide a friendly and concise answer.
    """

        synthesis_response = ollama.chat(
            model=self.__model,
            messages=[
                {
                    "role": "user",
                    "content": synthesis_prompt
                }
            ]
        )

        return {
            "user_request": user_prompt,
            "tool_used": tool_name,
            "tool_result": tool_result,
            "agent_response": synthesis_response["message"]["content"]
        }

    def _parse_section(self, text, section_name):
        items = []
        in_section = False
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.upper().startswith(section_name.upper()):
                in_section = True
                continue
            if in_section:
                if line.startswith("-"):
                    items.append(line[1:].strip())
                elif line.endswith(":") and line.isupper():
                    break
        return items