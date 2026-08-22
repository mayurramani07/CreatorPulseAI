function DemandChart({ recommendations = [] }) {
  if (!recommendations.length) {
    return null;
  }

  const maxScore = Math.max(
    ...recommendations.map((item) =>
      Number(item?.demand_score ?? 0)
    ),
    1
  );

  return (
    <section className="mt-16">
      <div className="mb-7">
        <p className="text-xs font-medium uppercase tracking-[0.14em] text-violet-400/80">
          Demand Overview
        </p>

        <h2 className="mt-2 text-2xl font-semibold tracking-tight text-zinc-100 sm:text-3xl">
          What topics are in demand?
        </h2>

        <p className="mt-2 text-sm text-zinc-500">
          Compare audience demand across identified topics.
        </p>
      </div>

      <div className="rounded-2xl border border-white/[0.07] bg-white/[0.025] p-5 backdrop-blur-xl sm:p-6">
        <div className="flex flex-col gap-5">
          {recommendations.map((item, index) => {
            const score = Number(
              item?.demand_score ?? 0
            );

            const width = Math.max(
              (score / maxScore) * 100,
              score > 0 ? 4 : 0
            );

            return (
              <div key={`${item.topic}-${index}`}>
                <div className="mb-2 flex items-center justify-between gap-4">
                  <div className="flex min-w-0 items-center gap-3">
                    <span className="w-6 text-[10px] font-medium text-zinc-600">
                      {String(index + 1).padStart(2, "0")}
                    </span>

                    <span className="truncate text-sm font-medium text-zinc-300">
                      {item?.topic || "Unknown Topic"}
                    </span>
                  </div>

                  <span className="shrink-0 text-sm font-semibold text-violet-400">
                    {score.toFixed(2)}
                  </span>
                </div>

                <div className="ml-9 h-2 overflow-hidden rounded-full bg-white/[0.05]">
                  <div
                    className="h-full rounded-full bg-violet-500/70 transition-all duration-700"
                    style={{
                      width: `${width}%`,
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

export default DemandChart;