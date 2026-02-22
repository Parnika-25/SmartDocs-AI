import { useEffect, useState } from "react";
import axios from "axios";

export default function SystemHealth() {
  const [health, setHealth] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    axios
      .get("https://pdf-ai-app-bm00.onrender.com/health")
      .then((res) => setHealth(res.data.components))
      .catch(() => setError("Unable to fetch system health"));
  }, []);

  if (error) {
    return <small style={{ color: "red" }}>⚠ {error}</small>;
  }

  if (!health) {
    return <small>🔄 Checking system health...</small>;
  }

  return (
    <div
      style={{
        background: "#111",
        padding: "10px 14px",
        borderRadius: "8px",
        fontSize: "13px",
        color: "#ccc",
        marginTop: "8px",
      }}
    >
      <strong style={{ color: "#fff" }}>🛠 System Health</strong>

      <div>📦 Vector DB: {health.vector_db}</div>
      <div>🔑 OpenAI: {health.openai}</div>
    </div>
  );
}
