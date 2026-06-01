"""
test_health_system.py
Evaluare si testare a sistemului de monitorizare a sanatatii.
Acopera: analysis.py, trend_analysis.py, report_generator.py, utils.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analize.analysis import analyze_heart_rate, analyze_sleep, calculate_health_score
from analize.trend_analysis import analyze_steps_trend, analyze_sleep_trend, generate_health_insights
from analize.report_generator import generate_weekly_report
from storage.utils import validate_data, generate_recommendations


PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"

results = {"passed": 0, "failed": 0, "total": 0}


def check(description, condition):
    results["total"] += 1
    if condition:
        results["passed"] += 1
        print(f"  {PASS} {description}")
    else:
        results["failed"] += 1
        print(f"  {FAIL} {description}")


print("\n" + "="*60)
print(" HEALTH MONITOR — TEST SUITE")
print("="*60)


print("\n[1] analyze_heart_rate()")

r = analyze_heart_rate([72, 75, 80])
check("Returns success status", r["status"] == "success")
check("Average is correct", abs(r["average_heart_rate"] - 75.67) < 0.1)
check("Condition is normal for 72-80 BPM", r["condition"] == "normal")

r = analyze_heart_rate([110, 120])
check("High heart rate detected", r["condition"] == "high")

r = analyze_heart_rate([45, 50])
check("Low heart rate detected", r["condition"] == "low")

r = analyze_heart_rate([])
check("Empty list returns error", r["status"] == "error")


print("\n[2] analyze_sleep()")

r = analyze_sleep(8.0)
check("8h sleep → good quality", r["sleep_quality"] == "good")
check("8h sleep → score 100", r["sleep_score"] == 100)

r = analyze_sleep(5.5)
check("5.5h sleep → average quality", r["sleep_quality"] == "average")

r = analyze_sleep(3.0)
check("3h sleep → poor quality", r["sleep_quality"] == "poor")

r = analyze_sleep(10.0)
check("10h sleep → oversleep", r["sleep_quality"] == "oversleep")

r = analyze_sleep(-1)
check("Negative hours → error", r["status"] == "error")


print("\n[3] calculate_health_score()")

r = calculate_health_score([72], 8.0, 10000)
check("Healthy profile → score >= 85", r.get("health_score", 0) >= 85)
check("Healthy profile → excellent status", r.get("health_status") == "excellent")

r = calculate_health_score([115], 4.0, 1000)
check("Unhealthy profile → score < 50", r.get("health_score", 100) < 50)
check("Unhealthy profile → poor status", r.get("health_status") == "poor")

r = calculate_health_score([72], 7.0, 7000)
check("Average profile → score between 50-84", 50 <= r.get("health_score", 0) <= 84)


print("\n[4] analyze_steps_trend()")

r = analyze_steps_trend([5000, 6000, 7000, 8000, 9000])
check("Increasing steps → trend = increasing", r["trend"] == "increasing")

r = analyze_steps_trend([9000, 8000, 7000, 6000, 5000])
check("Decreasing steps → trend = decreasing", r["trend"] == "decreasing")

r = analyze_steps_trend([8000, 8100, 7900, 8000])
check("Stable steps → trend = stable", r["trend"] == "stable")

r = analyze_steps_trend([])
check("Empty list → error", r["status"] == "error")


print("\n[5] analyze_sleep_trend()")

r = analyze_sleep_trend([6, 6.5, 7, 7.5, 8])
check("Improving sleep → trend = increasing", r["trend"] == "increasing")

r = analyze_sleep_trend([8, 7, 6, 5])
check("Worsening sleep → trend = decreasing", r["trend"] == "decreasing")


print("\n[6] generate_health_insights()")

r = generate_health_insights(
    [9000, 8000, 7000, 6000],
    [7, 6, 5, 4]
)
check("Returns success status", r["status"] == "success")
check("Has insights list", isinstance(r["insights"], list))
check("Detects decreasing activity", any("Physical" in i or "activity" in i.lower() for i in r["insights"]))
check("Detects sleep deficit", any("sleep" in i.lower() for i in r["insights"]))


print("\n[7] generate_weekly_report()")

hr = [70, 75, 72, 80, 68, 77, 74]
sleep = [7, 6.5, 8, 7.5, 6, 8, 7]
steps = [8000, 6000, 10000, 9000, 5000, 11000, 7500]

r = generate_weekly_report(hr, sleep, steps)
check("Returns success status", r["status"] == "success")
check("Average heart rate is correct", abs(r["average_heart_rate"] - sum(hr)/len(hr)) < 0.1)
check("Best day is day 6 (max steps)", r["best_day"] == 6)
check("Worst day is day 5 (min steps)", r["worst_day"] == 5)
check("Max steps correct", r["maximum_steps"] == 11000)

r = generate_weekly_report([], sleep, steps)
check("Missing data → error", r["status"] == "error")


print("\n[8] validate_data()")

ok, msg = validate_data({"heart_rate": 72, "sleep_hours": 7.5})
check("Valid data passes", ok)

ok, msg = validate_data({"heart_rate": 72})
check("Missing sleep_hours → invalid", not ok)

ok, msg = validate_data({"heart_rate": 250, "sleep_hours": 7})
check("Heart rate 250 → invalid", not ok)

ok, msg = validate_data({"heart_rate": 72, "sleep_hours": 25})
check("Sleep 25h → invalid", not ok)


print("\n[9] generate_recommendations()")

recs = generate_recommendations({"heart_rate": 115, "sleep_hours": 4})
check("Generates recommendations list", isinstance(recs, list))
check("At least 2 recommendations", len(recs) >= 2)
check("Mentions sleep issue", any("sleep" in r.lower() for r in recs))
check("Mentions heart rate issue", any("heart" in r.lower() for r in recs))

recs = generate_recommendations({"heart_rate": 72, "sleep_hours": 8})
check("Healthy user → positive recommendations", any("normal" in r.lower() or "healthy" in r.lower() for r in recs))


print("\n" + "="*60)
total = results["total"]
passed = results["passed"]
failed = results["failed"]
pct = round(passed / total * 100) if total > 0 else 0
print(f" RESULTS: {passed}/{total} passed ({pct}%)")
if failed > 0:
    print(f" {failed} test(s) FAILED — review logic above")
else:
    print(" All tests passed!")
print("="*60 + "\n")