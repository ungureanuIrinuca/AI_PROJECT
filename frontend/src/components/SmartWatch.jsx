import { useState, useEffect } from "react";

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
    const [activeTab, setActiveTab] = useState("monitor");

    // Trend & History
    const [history, setHistory] = useState([]);
    const [weeklyReport, setWeeklyReport] = useState(null);
    const [reportLoading, setReportLoading] = useState(false);

    // Chat cu agentul
    const [chatInput, setChatInput] = useState("");
    const [chatMessages, setChatMessages] = useState([
        { role: "assistant", text: "Hi! I'm your health AI agent. Ask me anything about your health data." }
    ]);
    const [chatLoading, setChatLoading] = useState(false);

    const currentTime = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

    const syncWearableData = () => {
        const healthyDay = Math.random() > 0.5;

        let newHR, newSleep, newSteps, newCalories;

        if (healthyDay) {
            newHR = Math.floor(Math.random() * 20) + 65;
            newSleep = parseFloat((Math.random() * 2 + 7).toFixed(1));
            newSteps = Math.floor(Math.random() * 4000) + 8000;
            newCalories = Math.floor(Math.random() * 300) + 500;
        } else {
            newHR = Math.floor(Math.random() * 30) + 100;
            newSleep = parseFloat((Math.random() * 2 + 3).toFixed(1));
            newSteps = Math.floor(Math.random() * 2500) + 500;
            newCalories = Math.floor(Math.random() * 200) + 150;
        }

        setHeartRate(newHR);
        setSleepHours(newSleep);
        setSteps(newSteps);
        setCalories(newCalories);

        // Adauga in istoric
        setHistory(prev => [
            ...prev.slice(-6),
            { heart_rate: newHR, sleep_hours: newSleep, steps: newSteps, calories: newCalories, date: new Date().toLocaleDateString() }
        ]);

        setHealthScore(null);
        setHealthStatus(null);
        setInsights([]);
        setRecommendations([]);
        setWeeklyReport(null);
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

    const loadWeeklyReport = async () => {
        if (history.length < 2) {
            alert("Sincronizeaza cel putin 2 zile de date pentru raport saptamanal.");
            return;
        }
        setReportLoading(true);
        try {
            const response = await fetch("http://127.0.0.1:5000/weekly-report", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ history })
            });
            const data = await response.json();
            setWeeklyReport(data);
        } catch (error) {
            // Fallback local
            const avgHR = Math.round(history.reduce((s, d) => s + d.heart_rate, 0) / history.length);
            const avgSleep = (history.reduce((s, d) => s + d.sleep_hours, 0) / history.length).toFixed(1);
            const avgSteps = Math.round(history.reduce((s, d) => s + d.steps, 0) / history.length);
            setWeeklyReport({
                average_heart_rate: avgHR,
                average_sleep: avgSleep,
                average_steps: avgSteps,
                best_day: history.reduce((best, d, i) => d.steps > history[best].steps ? i : best, 0) + 1,
                worst_day: history.reduce((worst, d, i) => d.steps < history[worst].steps ? i : worst, 0) + 1,
                status: "success"
            });
        } finally {
            setReportLoading(false);
        }
    };

    const sendChat = async () => {
        if (!chatInput.trim()) return;
        const userMsg = chatInput.trim();
        setChatInput("");
        setChatMessages(prev => [...prev, { role: "user", text: userMsg }]);
        setChatLoading(true);

        try {
            const currentData = heartRate !== "--" ? {
                heart_rate: Number(heartRate),
                sleep_hours: Number(sleepHours),
                steps: Number(steps),
                calories: Number(calories)
            } : {};

            const response = await fetch("http://127.0.0.1:5000/agent-chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: userMsg, user_data: currentData })
            });
            const data = await response.json();
            const agentText = data.agent_response || "I couldn't process that request.";
            setChatMessages(prev => [...prev, { role: "assistant", text: agentText }]);
        } catch (error) {
            setChatMessages(prev => [...prev, {
                role: "assistant",
                text: "⚠️ Backend unavailable. Make sure Flask is running on port 5000."
            }]);
        } finally {
            setChatLoading(false);
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

            {/* Tab Navigation */}
            <div className="tabs">
                {["monitor", "trends", "chat"].map(tab => (
                    <button
                        key={tab}
                        className={`tab-btn ${activeTab === tab ? "tab-active" : ""}`}
                        onClick={() => setActiveTab(tab)}
                    >
                        {tab === "monitor" ? "📊 Monitor" : tab === "trends" ? "📈 Trends" : "🤖 Agent"}
                    </button>
                ))}
            </div>

            {/* TAB: Monitor */}
            {activeTab === "monitor" && (
                <>
                    <div className="metric-card"><span>❤️ Heart Rate</span><strong>{heartRate} {heartRate !== "--" ? "BPM" : ""}</strong></div>
                    <div className="metric-card"><span>😴 Sleep</span><strong>{sleepHours} {sleepHours !== "--" ? "h" : ""}</strong></div>
                    <div className="metric-card"><span>👟 Steps</span><strong>{steps}</strong></div>
                    <div className="metric-card"><span>🔥 Calories</span><strong>{calories}</strong></div>

                    <button className="sync-btn" onClick={syncWearableData}>Sync Wearable Data</button>
                    <button
                        className="analyze-btn"
                        onClick={analyzeHealth}
                        disabled={loading}
                    >
                        {loading ? "🤖 Analyzing..." : "Analyze Health"}
                    </button>


                    {healthScore !== null && (
                        <div className="health-score">

                            <div className="score-text">
                                Health Score — <span
                                style={{color: statusColor[healthStatus] || "#00d4ff"}}>{healthStatus?.toUpperCase()}</span>
                            </div>
                            <div className="score-value" style={{color: statusColor[healthStatus] || "#00d4ff"}}>
                                {healthScore}
                            </div>
                        </div>
                    )}

                    {insights.length > 0 && (
                        <div className="recommendations">
                            <div style={{ color: "#00d4ff", marginBottom: 8, fontWeight: "bold" }}>📊 Insights</div>
                            {insights.map((insight, i) => (
                                <div key={i} className="recommendation-card" style={{ borderLeft: "3px solid #00d4ff" }}>{insight}</div>
                            ))}
                        </div>
                    )}

                    {recommendations.length > 0 && (
                        <div className="recommendations">
                            <div style={{ color: "#22c55e", marginBottom: 8, fontWeight: "bold" }}>💡 Recommendations</div>
                            {recommendations.map((rec, i) => (
                                <div key={i} className="recommendation-card" style={{ borderLeft: "3px solid #22c55e" }}>{rec}</div>
                            ))}
                        </div>
                    )}
                </>
            )}

            {/* TAB: Trends */}
            {activeTab === "trends" && (
                <>
                    <div style={{ color: "#9ca3af", fontSize: 13, marginBottom: 12 }}>
                        {history.length === 0
                            ? "No history yet. Sync data on the Monitor tab first."
                            : `${history.length} day(s) of data recorded.`}
                    </div>

                    {history.length > 0 && (
                        <div className="history-list">
                            {history.map((d, i) => (
                                <div key={i} className="metric-card" style={{ fontSize: 12 }}>
                                    <span style={{ color: "#9ca3af" }}>Day {i + 1}</span>
                                    <span>❤️ {d.heart_rate} · 😴 {d.sleep_hours}h · 👟 {d.steps}</span>
                                </div>
                            ))}
                        </div>
                    )}

                    <button className="sync-btn" onClick={loadWeeklyReport} style={{ marginTop: 12 }}>
                        {reportLoading ? "Loading..." : "Generate Weekly Report"}
                    </button>

                    {weeklyReport && weeklyReport.status === "success" && (
                        <div className="recommendations" style={{ marginTop: 16 }}>
                            <div style={{ color: "#00d4ff", marginBottom: 8, fontWeight: "bold" }}>📋 Weekly Summary</div>
                            {[
                                ["Avg Heart Rate", `${weeklyReport.average_heart_rate} BPM`],
                                ["Avg Sleep", `${weeklyReport.average_sleep} h`],
                                ["Avg Steps", weeklyReport.average_steps],
                                ["Best Day", `Day ${weeklyReport.best_day}`],
                                ["Worst Day", `Day ${weeklyReport.worst_day}`],
                            ].map(([label, value]) => (
                                <div key={label} className="metric-card" style={{ fontSize: 13 }}>
                                    <span>{label}</span><strong>{value}</strong>
                                </div>
                            ))}
                        </div>
                    )}
                </>
            )}

            {/* TAB: Agent Chat */}
            {activeTab === "chat" && (
                <>
                    <div className="chat-window">
                        {chatMessages.map((msg, i) => (
                            <div key={i} className={`chat-msg ${msg.role === "user" ? "chat-user" : "chat-agent"}`}>
                                {msg.text}
                            </div>
                        ))}
                        {chatLoading && <div className="chat-msg chat-agent" style={{ color: "#6b7280" }}>Thinking...</div>}
                    </div>
                    <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
                        <input
                            className="chat-input"
                            value={chatInput}
                            onChange={e => setChatInput(e.target.value)}
                            onKeyDown={e => e.key === "Enter" && sendChat()}
                            placeholder="Ask about your health..."
                        />
                        <button className="analyze-btn" style={{ width: "auto", padding: "8px 16px" }} onClick={sendChat}>
                            Send
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}

export default SmartWatch;