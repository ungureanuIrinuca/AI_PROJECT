def analyze_heart_rate(hr):

    if hr > 100:
        return "High heart rate"

    if hr < 50:
        return "Low heart rate"

    return "Normal heart rate"


def analyze_sleep(hours):

    if hours < 6:
        return "Insufficient sleep"

    return "Healthy sleep duration"


def calculate_health_score(hr, sleep):

    score = 100

    if hr > 100 or hr < 50:
        score -= 20

    if sleep < 6:
        score -= 30

    return max(score, 0)


def analyze_health(data):

    heart_rate = data["heart_rate"]
    sleep_hours = data["sleep_hours"]

    heart_result = analyze_heart_rate(heart_rate)
    sleep_result = analyze_sleep(sleep_hours)

    score = calculate_health_score(
        heart_rate,
        sleep_hours
    )

    return {
        "heart_rate_analysis": heart_result,
        "sleep_analysis": sleep_result,
        "health_score": score
    }