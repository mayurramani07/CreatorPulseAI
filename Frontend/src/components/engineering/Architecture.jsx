function Architecture() {
  return (
    <section className="mt-16">
      <div className="mb-8">
        <p className="text-xs font-medium uppercase tracking-[0.14em] text-violet-400/80">
          System Architecture
        </p>

        <h2 className="mt-3 text-2xl font-semibold tracking-tight text-zinc-100 sm:text-3xl">
          From YouTube comments to audience intelligence.
        </h2>

        <p className="mt-3 max-w-2xl text-sm leading-6 text-zinc-500">
          CreatorPulseAI processes audience feedback through a
          multi-stage pipeline before producing ranked content
          opportunities.
        </p>
      </div>

      <div className="overflow-x-auto rounded-2xl border border-white/[0.07] bg-white/[0.025] p-6 backdrop-blur-xl sm:p-8">
        <div className="min-w-[900px]">

          <div className="flex items-center gap-3">

            <ArchitectureNode
              title="React"
              subtitle="Frontend"
            />

            <Arrow />

            <ArchitectureNode
              title="FastAPI"
              subtitle="API Layer"
            />

            <Arrow />

            <ArchitectureNode
              title="YouTube API"
              subtitle="Data Source"
            />

          </div>

          <div className="my-8 ml-[190px] h-10 w-px bg-white/[0.08]" />

          <div className="ml-[110px] flex items-center gap-3">

            <ArchitectureNode
              title="Sampling"
              subtitle="Comment Selection"
            />

            <Arrow />

            <ArchitectureNode
              title="Preprocessing"
              subtitle="Text Cleaning"
            />

            <Arrow />

            <ArchitectureNode
              title="Embeddings"
              subtitle="Semantic Detection"
            />

          </div>

          <div className="my-8 ml-[500px] h-10 w-px bg-white/[0.08]" />

          <div className="ml-[360px] flex items-center gap-3">

            <ArchitectureNode
              title="GPT-OSS 20B"
              subtitle="Topic Grouping"
              highlight
            />

            <Arrow />

            <ArchitectureNode
              title="Demand Scoring"
              subtitle="Ranking"
            />

          </div>

          <div className="my-8 ml-[575px] h-10 w-px bg-white/[0.08]" />

          <div className="ml-[475px]">
            <ArchitectureNode
              title="Audience Insights"
              subtitle="Content Opportunities"
              highlight
            />
          </div>

        </div>
      </div>
    </section>
  );
}

function ArchitectureNode({
  title,
  subtitle,
  highlight = false,
}) {
  return (
    <div
      className={`w-48 shrink-0 rounded-xl border p-4 transition-colors ${
        highlight
          ? "border-violet-400/25 bg-violet-500/[0.07]"
          : "border-white/[0.07] bg-[#11121a]"
      }`}
    >
      <p
        className={`text-sm font-semibold ${
          highlight
            ? "text-violet-300"
            : "text-zinc-200"
        }`}
      >
        {title}
      </p>

      <p className="mt-1 text-xs text-zinc-600">
        {subtitle}
      </p>
    </div>
  );
}

function Arrow() {
  return (
    <div className="flex items-center text-zinc-700">
      <span className="h-px w-8 bg-white/[0.08]" />
      <span className="text-xs">›</span>
    </div>
  );
}

export default Architecture;