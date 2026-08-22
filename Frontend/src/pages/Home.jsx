import { useState } from "react";

import Hero from "../components/Hero";
import AnalysisSection from "../components/AnalysisSection";

import { analyzeVideo } from "../services/api";

function Home() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze(videoId) {
    setError("");
    setAnalysis(null);

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
    <main>
      <Hero
        onAnalyze={handleAnalyze}
        loading={loading}
        error={error}
      />

      {analysis && (
        <AnalysisSection analysis={analysis} />
      )}
    </main>
  );
}

export default Home;