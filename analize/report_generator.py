def generate_weekly_report(
        heart_rate_history,
        sleep_history,
        steps_history):
    """
    Genereaza un raport saptamanal
    pe baza datelor colectate.
    """

    if (
            not heart_rate_history
            or not sleep_history
            or not steps_history
    ):
        return {
            "status": "error",
            "message": "Missing historical data"
        }

    average_heart_rate = (
        sum(heart_rate_history)
        / len(heart_rate_history)
    )

    average_sleep = (
        sum(sleep_history)
        / len(sleep_history)
    )

    average_steps = (
        sum(steps_history)
        / len(steps_history)
    )

    best_day_index = steps_history.index(
        max(steps_history)
    )

    worst_day_index = steps_history.index(
        min(steps_history)
    )

    return {
        "status": "success",

        "average_heart_rate":
            round(
                average_heart_rate,
                2
            ),

        "average_sleep":
            round(
                average_sleep,
                2
            ),

        "average_steps":
            round(
                average_steps,
                2
            ),

        "best_day":
            best_day_index + 1,

        "worst_day":
            worst_day_index + 1,

        "maximum_steps":
            max(steps_history),

        "minimum_steps":
            min(steps_history),

        "maximum_sleep":
            max(sleep_history),

        "minimum_sleep":
            min(sleep_history),

        "maximum_heart_rate":
            max(heart_rate_history),

        "minimum_heart_rate":
            min(heart_rate_history)
    }