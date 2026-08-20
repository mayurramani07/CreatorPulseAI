import { useState } from "react";

import "./App.css";

import { analyzeVideo } from "./services/api";

function App() {
  const [videoUrl, setVideoUrl] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [analysis, setAnalysis] = useState(null);

  function extractVideoId(url) {
    try {
      const parsedUrl = new URL(url);

      if (
        parsedUrl.hostname === "www.youtube.com" ||
        parsedUrl.hostname === "youtube.com"
      ) {
        return parsedUrl.searchParams.get("v");
      }

      if (parsedUrl.hostname === "youtu.be") {
        return parsedUrl.pathname.slice(1);
      }

      return null;
    } catch {
      return null;
    }
  }

  async function handleAnalyze() {
    setError("");
    setAnalysis(null);

    const videoId = extractVideoId(videoUrl);

    if (!videoId) {
      setError(
        "Please enter a valid YouTube video URL."
      );

      return;
    }

    try {
      setLoading(true);

      const data = await analyzeVideo(videoId);

      setAnalysis(data);
    } catch (err) {
      setError(
        err.message ||
        "Something went wrong while analyzing the video."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <main className="hero">

        <div className="badge">
          AI-Powered Audience Intelligence
        </div>

        <h1>
          CreatorPulse
          <span>AI</span>
        </h1>

        <p className="hero-description">
          Turn YouTube comments into actionable
          content opportunities.
        </p>

        <div className="analyzer-card">

          <input
            type="text"
            value={videoUrl}
            onChange={(event) =>
              setVideoUrl(event.target.value)
            }
            placeholder="Paste your YouTube video URL..."
          />

          <button
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading
              ? "Analyzing..."
              : "Analyze Audience"}
          </button>

        </div>

        {error && (
          <p className="error-message">
            {error}
          </p>
        )}

        {analysis && (
          <div className="result-preview">

            <h2>
              Analysis Complete
            </h2>

            <p>
              Comments analyzed:{" "}
              {analysis.processed_comments}
            </p>

            <p>
              Content requests:{" "}
              {analysis.content_request_candidates}
            </p>

            <p>
              Topics identified:{" "}
              {analysis.topic_groups}
            </p>

          </div>
        )}

      </main>
    </div>
  );
}

export default App;