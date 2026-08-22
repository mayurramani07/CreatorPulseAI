function AnalysisLoader() {
  return (
    <div className="mx-auto mt-10 w-full max-w-3xl">
      <div className="rounded-2xl border border-white/[0.07] bg-white/[0.025] px-6 py-10 text-center backdrop-blur-xl sm:px-10">

        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full border border-violet-400/20 bg-violet-500/[0.08]">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-violet-400/20 border-t-violet-400" />
        </div>

        <h2 className="mt-6 text-xl font-semibold tracking-tight text-zinc-100">
          Analyzing your audience
        </h2>

        <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-zinc-500">
          CreatorPulseAI is processing the video's comments
          and identifying content opportunities.
        </p>

        <div className="mx-auto mt-7 flex max-w-sm flex-col gap-3 text-left">

          <LoadingStep
            number="01"
            text="Collecting YouTube comments"
          />

          <LoadingStep
            number="02"
            text="Processing audience feedback"
          />

          <LoadingStep
            number="03"
            text="Detecting content requests"
          />

          <LoadingStep
            number="04"
            text="Finding content opportunities"
          />

        </div>

        <p className="mt-7 text-xs text-zinc-700">
          This may take a few moments.
        </p>

      </div>
    </div>
  );
}

function LoadingStep({ number, text }) {
  return (
    <div className="flex items-center gap-3 rounded-lg border border-white/[0.05] bg-white/[0.015] px-4 py-3">

      <span className="text-[10px] font-medium tracking-wider text-violet-400/70">
        {number}
      </span>

      <span className="text-xs text-zinc-500">
        {text}
      </span>

    </div>
  );
}

export default AnalysisLoader;