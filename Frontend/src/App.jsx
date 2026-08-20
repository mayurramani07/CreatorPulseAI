import { useState } from "react";

import "./App.css";

import { analyzeVideo } from "./services/api";

import StatsCard from "./components/StatsCard";

import RecommendationCard from "./components/RecommendationCard";


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
          <>

            {/* ---------------------------------- */}
            {/* Analysis Overview */}
            {/* ---------------------------------- */}

            <div className="analysis-header">

              <h2>
                Audience Analysis
              </h2>

              <p>
                Here's what your audience is asking for.
              </p>

            </div>


            {/* ---------------------------------- */}
            {/* Statistics */}
            {/* ---------------------------------- */}

            <div className="stats-grid">

              <StatsCard
                label="Comments Analyzed"
                value={analysis.processed_comments}
                description="Comments processed by CreatorPulse"
              />


              <StatsCard
                label="Content Requests"
                value={
                  analysis.content_request_candidates
                }
                description="Audience requests detected"
              />


              <StatsCard
                label="Topics Identified"
                value={analysis.topic_groups}
                description="Distinct content opportunities"
              />

            </div>


            {/* ---------------------------------- */}
            {/* Content Opportunities */}
            {/* ---------------------------------- */}

            <div className="recommendations-section">

              <div className="recommendations-header">

                <h2>
                  Top Content Opportunities
                </h2>

                <p>
                  Topics your audience is most interested in.
                </p>

              </div>


              <div className="recommendations-list">

                {analysis.recommendations &&
                  analysis.recommendations.map(
                    (recommendation, index) => (

                      <RecommendationCard
                        key={`${recommendation.topic}-${index}`}
                        rank={index + 1}
                        recommendation={recommendation}
                      />

                    )
                  )}

              </div>

            </div>

          </>
        )}

      </main>

    </div>
  );
}


export default App;