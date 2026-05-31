def analyze_steps_trend(steps_history):

    if not steps_history:
        return {
            "status": "error",
            "message": "No steps data provided"
        }

    average_steps = sum(steps_history) / len(steps_history)

    first_day = steps_history[0]
    last_day = steps_history[-1]

    if first_day == 0:
        change_percent = 0
    else:
        change_percent = (
            (last_day - first_day)
            / first_day
        ) * 100

    if change_percent > 5:
        trend = "increasing"

    elif change_percent < -5:
        trend = "decreasing"

    else:
        trend = "stable"

    return {
        "status": "success",
        "average_steps": round(average_steps, 2),
        "trend": trend,
        "change_percent": round(change_percent, 2)
    }


def analyze_sleep_trend(sleep_history):

    if not sleep_history:
        return {
            "status": "error",
            "message": "No sleep data provided"
        }

    average_sleep = (
        sum(sleep_history)
        / len(sleep_history)
    )

    first_day = sleep_history[0]
    last_day = sleep_history[-1]

    if first_day == 0:
        change_percent = 0
    else:
        change_percent = (
            (last_day - first_day)
            / first_day
        ) * 100

    if change_percent > 5:
        trend = "increasing"

    elif change_percent < -5:
        trend = "decreasing"

    else:
        trend = "stable"

    return {
        "status": "success",
        "average_sleep": round(
            average_sleep,
            2
        ),
        "trend": trend,
        "change_percent": round(
            change_percent,
            2
        )
    }


def generate_health_insights(
        steps_history,
        sleep_history):

    steps_result = analyze_steps_trend(
        steps_history
    )

    sleep_result = analyze_sleep_trend(
        sleep_history
    )

    insights = []

    if steps_result["trend"] == "decreasing":
        insights.append(
            "Physical activity is decreasing."
        )

    if sleep_result["trend"] == "decreasing":
        insights.append(
            "Sleep duration is decreasing."
        )

    if (
            sleep_result["status"] == "success"
            and
            sleep_result["average_sleep"] < 6
    ):
        insights.append(
            "Potential sleep deficit detected."
        )

    return {
        "status": "success",
        "steps_analysis": steps_result,
        "sleep_analysis": sleep_result,
        "insights": insights
    }