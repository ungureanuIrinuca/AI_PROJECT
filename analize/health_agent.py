import json
import ollama

from analysis import (
    analyze_heart_rate,
    analyze_sleep,
    calculate_health_score
)

from trend_analysis import (
    generate_health_insights
)

from report_generator import (
    generate_weekly_report
)


class HealthAgent:

    def __init__(self, model="mistral"):
        self.__model = model

    def __select_tool(self, user_prompt):

        system_prompt = """
        You are a routing agent.

        Available tools:

        heart_rate_analysis
        sleep_analysis
        health_score
        trend_analysis
        weekly_report

        Return ONLY the tool name.
        """

        response = ollama.chat(
            model=self.__model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        return response["message"]["content"].strip()

    def process_request(
            self,
            user_prompt,
            data):

        selected_tool = self.__select_tool(
            user_prompt
        )

        if selected_tool == "heart_rate_analysis":

            result = analyze_heart_rate(
                data["heart_rate"]
            )

        elif selected_tool == "sleep_analysis":

            result = analyze_sleep(
                data["sleep_hours"]
            )

        elif selected_tool == "health_score":

            result = calculate_health_score(
                data["heart_rate"],
                data["sleep_hours"],
                data["steps"]
            )

        elif selected_tool == "trend_analysis":

            result = generate_health_insights(
                data["steps_history"],
                data["sleep_history"]
            )

        elif selected_tool == "weekly_report":

            result = generate_weekly_report(
                data["heart_rate_history"],
                data["sleep_history"],
                data["steps_history"]
            )

        else:

            return {
                "status": "error",
                "message":
                    f"Unknown tool: {selected_tool}"
            }

        explanation = ollama.chat(
            model=self.__model,
            messages=[
                {
                    "role": "system",
                    "content":
                    """
                    You are a health assistant.

                    Explain the result clearly.

                    Mention important observations.

                    Keep the explanation concise.
                    """
                },
                {
                    "role": "user",
                    "content":
                    f"Explain this analysis:\n{result}"
                }
            ]
        )

        return {
            "status": "success",
            "selected_tool":
                selected_tool,
            "tool_result":
                result,
            "llm_response":
                explanation["message"]["content"]
        }