import { useState } from "react";

import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import AnalysisSection from "./components/AnalysisSection";

import { analyzeVideo } from "./services/api";

function App() {
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
    <div className="min-h-screen bg-[#08090d] text-white">
      <Navbar />

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
    </div>
  );
}

export default App;