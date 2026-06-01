import pandas as pd

def load_data():
    return {
        "steps": pd.read_csv("data/dailySteps_merged.csv"),
        "sleep": pd.read_csv("data/sleepDay_merged.csv"),
        "calories": pd.read_csv("data/dailyCalories_merged.csv"),
        "intensity": pd.read_csv("data/dailyIntensities_merged.csv"),
        "heart": pd.read_csv("data/heartrate_seconds_merged.csv")
    }