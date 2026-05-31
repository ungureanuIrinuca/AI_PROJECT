# analysis.py

def analyze_heart_rate(heart_rate_data):
    """
    Analizeaza ritmul cardiac.

    Parametri:
        heart_rate_data - lista de valori heart rate

    Returneaza:
        dict cu statistici si status
    """

    if not heart_rate_data:
        return {
            "status": "error",
            "message": "No heart rate data provided"
        }

    avg_hr = sum(heart_rate_data) / len(heart_rate_data)
    min_hr = min(heart_rate_data)
    max_hr = max(heart_rate_data)

    # Clasificare simpla
    if avg_hr < 60:
        condition = "low"
    elif avg_hr <= 100:
        condition = "normal"
    else:
        condition = "high"

    return {
        "status": "success",
        "average_heart_rate": round(avg_hr, 2),
        "minimum_heart_rate": min_hr,
        "maximum_heart_rate": max_hr,
        "condition": condition
    }


def analyze_sleep(hours_slept):
    """
    Analizeaza calitatea somnului.

    Parametri:
        hours_slept - numar de ore dormite

    Returneaza:
        dict cu evaluarea somnului
    """

    if hours_slept < 0:
        return {
            "status": "error",
            "message": "Invalid sleep duration"
        }

    if hours_slept < 5:
        quality = "poor"
        score = 30

    elif hours_slept < 7:
        quality = "average"
        score = 70

    elif hours_slept <= 9:
        quality = "good"
        score = 100

    else:
        quality = "oversleep"
        score = 60

    return {
        "status": "success",
        "hours_slept": hours_slept,
        "sleep_quality": quality,
        "sleep_score": score
    }


def calculate_health_score(heart_rate_data, hours_slept, steps):
    """
    Calculeaza un scor general de sanatate.

    Parametri:
        heart_rate_data - lista valori heart rate
        hours_slept - ore dormite
        steps - numar pasi

    Returneaza:
        dict cu health score final
    """

    heart_rate_analysis = analyze_heart_rate(heart_rate_data)
    sleep_analysis = analyze_sleep(hours_slept)

    if heart_rate_analysis["status"] == "error":
        return heart_rate_analysis

    if sleep_analysis["status"] == "error":
        return sleep_analysis

    score = 0

    # Heart rate contribution
    if heart_rate_analysis["condition"] == "normal":
        score += 40

    elif heart_rate_analysis["condition"] == "low":
        score += 25

    else:
        score += 15

    # Sleep contribution
    score += sleep_analysis["sleep_score"] * 0.4

    # Steps contribution
    if steps >= 10000:
        score += 20

    elif steps >= 5000:
        score += 10

    else:
        score += 5

    final_score = min(round(score), 100)

    # Interpretare scor
    if final_score >= 85:
        health_status = "excellent"

    elif final_score >= 70:
        health_status = "good"

    elif final_score >= 50:
        health_status = "average"

    else:
        health_status = "poor"

    return {
        "status": "success",
        "health_score": final_score,
        "health_status": health_status,
        "heart_rate_analysis": heart_rate_analysis,
        "sleep_analysis": sleep_analysis,
        "steps": steps
    }


# Exemplu de testare
if __name__ == "__main__":

    heart_rate_values = [72, 75, 80, 77, 74]
    sleep_hours = 7.5
    daily_steps = 8500

    result = calculate_health_score(
        heart_rate_values,
        sleep_hours,
        daily_steps
    )

    print(result)



import pandas as pd
import os

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA = os.path.join(_BASE, "data")

steps_df = pd.read_csv(os.path.join(_DATA, "dailySteps_merged.csv"))
sleep_df = pd.read_csv(os.path.join(_DATA, "sleepDay_merged.csv"))
calories_df = pd.read_csv(os.path.join(_DATA, "dailyCalories_merged.csv"))
heart_df = pd.read_csv(os.path.join(_DATA, "heartrate_seconds_merged.csv"))

def average_steps():
    return round(steps_df["StepTotal"].mean(), 2)


def average_calories():
    return round(calories_df["Calories"].mean(), 2)


def average_sleep_hours():
    return round(
        sleep_df["TotalMinutesAsleep"].mean() / 60,
        2
    )


def average_heart_rate_dataset():
    return round(
        heart_df["Value"].mean(),
        2
    )





