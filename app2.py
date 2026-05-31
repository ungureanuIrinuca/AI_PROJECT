import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Health Monitor Dashboard")

heart_rate = st.number_input(
    "Heart Rate",
    min_value=30,
    max_value=220,
    value=75
)

sleep_hours = st.number_input(
    "Sleep Hours",
    min_value=0.0,
    max_value=24.0,
    value=7.0
)

steps = st.number_input(
    "Steps",
    min_value=0,
    value=8000
)

score = 100

if heart_rate > 100 or heart_rate < 50:
    score -= 20

if sleep_hours < 6:
    score -= 30

if steps < 5000:
    score -= 20

score = max(score, 0)

st.metric(
    "Health Score",
    score
)

if score > 80:
    st.success("Excellent health condition")
elif score > 60:
    st.warning("Average health condition")
else:
    st.error("Poor health condition")

data = pd.DataFrame({
    "Metric": [
        "Heart Rate",
        "Sleep",
        "Steps"
    ],
    "Value": [
        heart_rate,
        sleep_hours,
        steps
    ]
})

fig, ax = plt.subplots()

ax.bar(
    data["Metric"],
    data["Value"]
)

st.pyplot(fig)

st.subheader("Recommendation")

if score > 80:
    st.write(
        "Keep your current healthy lifestyle."
    )
elif score > 60:
    st.write(
        "Increase physical activity and sleep quality."
    )
else:
    st.write(
        "Improve sleep and daily exercise."
    )