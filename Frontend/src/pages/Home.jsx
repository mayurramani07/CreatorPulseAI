import { useState } from "react";

import Hero from "../components/Hero";
import AnalysisSection from "../components/AnalysisSection";
import AnalysisLoader from "../components/AnalysisLoader";
import ErrorMessage from "../components/ErrorMessage";
import VideoInfo from "../components/VideoInfo";

import {analyzeVideo, reanalyzeVideo} from "../services/api";


function Home() {
  const [analysis, setAnalysis] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [reanalyzing, setReanalyzing] =
    useState(false);

  const [error, setError] =
    useState("");


  async function handleAnalyze(
    videoId
  ) {
    setError("");
    setAnalysis(null);

    try {
      setLoading(true);

      const data =
        await analyzeVideo(videoId);

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


  async function handleReanalyze() {
    const videoId =
      analysis?.video?.id;

    if (!videoId) {
      setError(
        "Unable to re-analyze this video."
      );

      return;
    }

    setError("");

    try {
      setReanalyzing(true);

      const data =
        await reanalyzeVideo(videoId);

      const updatedAnalysis = {
        ...data,
        video: analysis.video,
      };

      setAnalysis(
        updatedAnalysis
      );

    } catch (err) {
      setError(
        err.message ||
          "Something went wrong while re-analyzing the video."
      );
    } finally {
      setReanalyzing(false);
    }
  }


  return (
    <main>
      <Hero
        onAnalyze={handleAnalyze}
        loading={loading}
        error={error}
      />

      <ErrorMessage
        message={error}
      />

      {loading && (
        <AnalysisLoader />
      )}

      {analysis && !loading && (
        <>
          <VideoInfo
            analysis={analysis}
          />

          <div className="mx-auto mt-5 flex w-full max-w-5xl justify-end px-5 sm:px-6 lg:px-8">
            <button
              type="button"
              onClick={handleReanalyze}
              disabled={reanalyzing}
              className="inline-flex items-center gap-2 rounded-xl border border-white/[0.08] bg-white/[0.025] px-4 py-2.5 text-sm font-medium text-zinc-300 transition-all duration-200 hover:border-violet-400/20 hover:bg-violet-500/[0.05] hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
            >
              {reanalyzing ? (
                <>
                  <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-zinc-600 border-t-violet-400" />
                  Re-analyzing...
                </>
              ) : (
                <>
                  <span className="text-violet-400">
                    ↻
                  </span>
                  Re-analyze
                </>
              )}
            </button>
          </div>

          <AnalysisSection
            analysis={analysis}
          />
        </>
      )}
    </main>
  );
}


export default Home;