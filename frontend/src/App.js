import React, { useState } from "react";
import "./App.css"; // Make sure App.css exists as below

function App() {
  const [file, setFile] = useState(null);
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState("");
  const [statusType, setStatusType] = useState(""); // "success" or "error"

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file || !email) {
      setStatus("Please upload a file and enter email");
      setStatusType("error");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("email", email);

    setStatus("Uploading and analyzing...");
    setStatusType("");

    try {
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.error) {
        setStatus("Error: " + data.error);
        setStatusType("error");
      } else {
        setStatus("Success! Summary emailed to you.");
        setStatusType("success");
      }
    } catch (err) {
      setStatus("Server error");
      setStatusType("error");
    }
  };

  return (
    <div className="app-container">
      <div className="card">
        <h2>Sales Insight Automator</h2>

        <form onSubmit={handleSubmit}>
          <input
            type="file"
            accept=".csv,.xlsx"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <button type="submit">Analyze Sales Data</button>
        </form>

        {status && (
          <p className={`status ${statusType}`}>{status}</p>
        )}
      </div>
    </div>
  );
}

export default App;