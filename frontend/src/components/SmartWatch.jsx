import { useState } from "react";

function SmartWatch() {

    const [heartRate, setHeartRate] = useState("--");
    const [sleepHours, setSleepHours] = useState("--");
    const [steps, setSteps] = useState("--");
    const [calories, setCalories] = useState("--");

    const [recommendations, setRecommendations] = useState([]);

    const [loading, setLoading] = useState(false);

    const currentTime = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

    const syncWearableData = () => {

        const healthyDay = Math.random() > 0.5;

        if (healthyDay) {

            setHeartRate(
                Math.floor(Math.random() * 20) + 65
            );

            setSleepHours(
                (Math.random() * 2 + 7).toFixed(1)
            );

            setSteps(
                Math.floor(Math.random() * 4000) + 8000
            );

            setCalories(
                Math.floor(Math.random() * 300) + 500
            );

        } else {

            setHeartRate(
                Math.floor(Math.random() * 30) + 100
            );

            setSleepHours(
                (Math.random() * 2 + 3).toFixed(1)
            );

            setSteps(
                Math.floor(Math.random() * 2500) + 500
            );

            setCalories(
                Math.floor(Math.random() * 200) + 150
            );
        }

        setRecommendations([]);
    };

    const analyzeHealth = async () => {

        if (heartRate === "--") {
            alert("Generate wearable data first!");
            return;
        }

        setLoading(true);

        try {

            const response = await fetch(
                "http://127.0.0.1:5000/analyze",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        heart_rate: Number(heartRate),
                        sleep_hours: Number(sleepHours),
                        steps: Number(steps),
                        calories: Number(calories)
                    })
                }
            );

            const data = await response.json();

            setRecommendations(
                data.recommendations || []
            );

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);

        }
    };

    return (

        <div className="watch">

            <div className="watch-time">
                {currentTime}
            </div>

            <div className="watch-header">
                ⌚ Health Monitor
            </div>

            <div className="metric-card">
                <span>❤️ Heart Rate</span>
                <strong>{heartRate} BPM</strong>
            </div>

            <div className="metric-card">
                <span>😴 Sleep</span>
                <strong>{sleepHours} h</strong>
            </div>

            <div className="metric-card">
                <span>👟 Steps</span>
                <strong>{steps}</strong>
            </div>

            <div className="metric-card">
                <span>🔥 Calories</span>
                <strong>{calories}</strong>
            </div>

            <button
                className="sync-btn"
                onClick={syncWearableData}
            >
                Sync Wearable Data
            </button>

            <button
                className="analyze-btn"
                onClick={analyzeHealth}
            >
                Analyze Health
            </button>

            {loading && (

                <div className="loading">
                    🤖 AI Analyzing...
                </div>

            )}

            <div className="recommendations">

                {recommendations.map((rec, index) => (

                    <div
                        key={index}
                        className="recommendation-card"
                    >
                        {rec}
                    </div>

                ))}

            </div>

        </div>

    );
}

export default SmartWatch;