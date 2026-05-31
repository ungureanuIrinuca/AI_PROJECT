import { useState } from "react";

function SmartWatch() {

    const [heartRate, setHeartRate] = useState("--");
    const [sleepHours, setSleepHours] = useState("--");
    const [steps, setSteps] = useState("--");
    const [calories, setCalories] = useState("--");

    const [healthScore, setHealthScore] = useState(null);
    const [healthStatus, setHealthStatus] = useState(null);
    const [insights, setInsights] = useState([]);
    const [recommendations, setRecommendations] = useState([]);

    const [loading, setLoading] = useState(false);

    const currentTime = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

    const syncWearableData = () => {

        const healthyDay = Math.random() > 0.5;

        if (healthyDay) {
            setHeartRate(Math.floor(Math.random() * 20) + 65);
            setSleepHours((Math.random() * 2 + 7).toFixed(1));
            setSteps(Math.floor(Math.random() * 4000) + 8000);
            setCalories(Math.floor(Math.random() * 300) + 500);
        } else {
            setHeartRate(Math.floor(Math.random() * 30) + 100);
            setSleepHours((Math.random() * 2 + 3).toFixed(1));
            setSteps(Math.floor(Math.random() * 2500) + 500);
            setCalories(Math.floor(Math.random() * 200) + 150);
        }

        // Reset rezultate anterioare
        setHealthScore(null);
        setHealthStatus(null);
        setInsights([]);
        setRecommendations([]);
    };

    const analyzeHealth = async () => {

        if (heartRate === "--") {
            alert("Apasa 'Sync Wearable Data' mai intai!");
            return;
        }

        setLoading(true);

        try {
            const response = await fetch("http://127.0.0.1:5000/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    heart_rate: Number(heartRate),
                    sleep_hours: Number(sleepHours),
                    steps: Number(steps),
                    calories: Number(calories)
                })
            });

            const data = await response.json();

            setHealthScore(data.health_score ?? null);
            setHealthStatus(data.health_status ?? null);
            setInsights(data.business_insights || []);
            setRecommendations(data.recommendations || []);

        } catch (error) {
            console.error("Eroare la analiza:", error);
            alert("Nu s-a putut conecta la backend. Verifica ca Flask ruleaza pe portul 5000.");
        } finally {
            setLoading(false);
        }
    };

    const statusColor = {
        excellent: "#22c55e",
        good: "#84cc16",
        average: "#f59e0b",
        poor: "#ef4444",
        unavailable: "#6b7280"
    };

    return (
        <div className="watch">

            <div className="watch-time">{currentTime}</div>
            <div className="watch-header">⌚ Health Monitor</div>

            {/* Metrici */}
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

            {/* Butoane */}
            <button className="sync-btn" onClick={syncWearableData}>
                Sync Wearable Data
            </button>
            <button className="analyze-btn" onClick={analyzeHealth}>
                Analyze Health
            </button>

            {loading && <div className="loading">🤖 AI Analyzing...</div>}

            {/* Health Score */}
            {healthScore !== null && (
                <div className="health-score">
                    <div
                        className="score-value"
                        style={{ color: statusColor[healthStatus] || "#00d4ff" }}
                    >
                        {healthScore}
                    </div>
                    <div className="score-text">
                        Health Score —{" "}
                        <span style={{ color: statusColor[healthStatus] || "#00d4ff" }}>
                            {healthStatus?.toUpperCase()}
                        </span>
                    </div>
                </div>
            )}

            {/* Business Insights */}
            {insights.length > 0 && (
                <div className="recommendations">
                    <div style={{ color: "#00d4ff", marginBottom: 8, fontWeight: "bold" }}>
                        📊 Insights
                    </div>
                    {insights.map((insight, index) => (
                        <div key={index} className="recommendation-card" style={{ borderLeft: "3px solid #00d4ff" }}>
                            {insight}
                        </div>
                    ))}
                </div>
            )}

            {/* Recomandari */}
            {recommendations.length > 0 && (
                <div className="recommendations">
                    <div style={{ color: "#22c55e", marginBottom: 8, fontWeight: "bold" }}>
                        💡 Recommendations
                    </div>
                    {recommendations.map((rec, index) => (
                        <div key={index} className="recommendation-card" style={{ borderLeft: "3px solid #22c55e" }}>
                            {rec}
                        </div>
                    ))}
                </div>
            )}

        </div>
    );
}

export default SmartWatch;