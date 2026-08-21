import { useState } from "react";

function Hero({
  onAnalyze,
  loading,
  error,
}) {
  const [videoUrl, setVideoUrl] = useState("");

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

  function handleSubmit() {
    const videoId = extractVideoId(videoUrl);

    if (!videoId) {
      return;
    }

    onAnalyze(videoId);
  }

  return (
    <section
      id="analyze"
      className="mx-auto flex min-h-[calc(100vh-64px)] w-full max-w-7xl items-center justify-center px-6 py-24 lg:px-8"
    >
      <div className="w-full max-w-3xl text-center">

        <div className="mb-7 inline-flex rounded-full border border-violet-400/20 bg-violet-500/[0.06] px-4 py-2">
          <span className="text-[10px] font-medium uppercase tracking-[0.12em] text-violet-300/80">
            AI-Powered Audience Intelligence
          </span>
        </div>

        <h1 className="text-5xl font-semibold tracking-[-0.045em] text-zinc-100 sm:text-4xl lg:text-5xl">
          Turn audience comments into{" "}
          <span className="text-violet-400">
            content opportunities.
          </span>
        </h1>

        <p className="mx-auto mt-4 max-w-2xl text-sm leading-7 text-zinc-500 sm:text-base">
          Analyze YouTube comments with AI and discover
          what your audience actually wants you to create.
        </p>

        <div className="mt-8">

          <div className="flex flex-col gap-2 rounded-2xl border border-white/[0.07] bg-white/[0.025] p-2 shadow-2xl shadow-black/20 backdrop-blur-xl sm:flex-row">

            <input
              type="text"
              value={videoUrl}
              onChange={(event) =>
                setVideoUrl(event.target.value)
              }
              placeholder="Paste your YouTube video URL..."
              className="min-w-0 flex-1 rounded-xl bg-transparent px-4 py-3 text-sm text-zinc-100 outline-none placeholder:text-zinc-600"
            />

            <button
              onClick={handleSubmit}
              disabled={loading}
              className="rounded-xl bg-violet-500 px-6 py-3 text-sm font-medium text-white transition hover:bg-violet-400 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading
                ? "Analyzing..."
                : "Analyze Audience"}
            </button>

          </div>

          {error && (
            <p className="mt-4 text-sm text-red-400">
              {error}
            </p>
          )}

        </div>

      </div>
    </section>
  );
}

export default Hero;