def validate_data(data):

    required_fields = [
        "heart_rate",
        "sleep_hours"
    ]

    for field in required_fields:

        if field not in data:
            return False, f"Missing field: {field}"

    heart_rate = data["heart_rate"]
    sleep_hours = data["sleep_hours"]

    if not isinstance(heart_rate, (int, float)):
        return False, "Heart rate must be a number"

    if not isinstance(sleep_hours, (int, float)):
        return False, "Sleep hours must be a number"

    if heart_rate < 30 or heart_rate > 220:
        return False, "Invalid heart rate value"

    if sleep_hours < 0 or sleep_hours > 24:
        return False, "Invalid sleep hours value"

    return True, "Valid data"


def normalize_heart_rate(hr):

    min_hr = 40
    max_hr = 200

    normalized = (hr - min_hr) / (max_hr - min_hr)

    return round(normalized, 2)


def normalize_sleep(hours):

    normalized = hours / 24

    return round(normalized, 2)


def normalize_data(data):

    return {
        "heart_rate": data["heart_rate"],
        "sleep_hours": data["sleep_hours"],
        "normalized_heart_rate":
            normalize_heart_rate(data["heart_rate"]),
        "normalized_sleep":
            normalize_sleep(data["sleep_hours"])
    }

def generate_recommendations(data):

    recommendations = []

    heart_rate = data["heart_rate"]
    sleep_hours = data["sleep_hours"]

    if sleep_hours < 6:
        recommendations.append(
            "You should increase your sleep duration to at least 7-8 hours per night."
        )

    elif sleep_hours > 9:
        recommendations.append(
            "You may be oversleeping. Monitor your sleep schedule."
        )

    else:
        recommendations.append(
            "Your sleep duration is within a healthy range."
        )

    if heart_rate > 100:
        recommendations.append(
            "Your heart rate is elevated. Consider reducing stress and consulting a healthcare professional if this persists."
        )

    elif heart_rate < 60:
        recommendations.append(
            "Your heart rate is lower than average. If you are not an athlete, consider a medical check-up."
        )

    else:
        recommendations.append(
            "Your heart rate is within the normal range."
        )

    if sleep_hours < 6 and heart_rate > 100:
        recommendations.append(
            "Insufficient sleep may contribute to an increased heart rate."
        )

    return recommendations