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