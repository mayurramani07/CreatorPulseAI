function RecommendationCard({
  recommendation,
  rank,
}) {
  const demandScore = Number(
    recommendation?.demand_score ?? 0
  );

  return (
    <article className="group rounded-2xl border border-white/[0.07] bg-white/[0.025] p-5 backdrop-blur-xl transition-all duration-300 hover:-translate-y-1 hover:border-violet-400/20 hover:bg-white/[0.04] sm:p-6">

      <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">

        <div className="min-w-0">
          <p className="text-[10px] font-medium uppercase tracking-[0.14em] text-zinc-600">
            Opportunity #{String(rank).padStart(2, "0")}
          </p>

          <h3 className="mt-2 break-words text-xl font-semibold tracking-tight text-zinc-100 sm:text-2xl">
            {recommendation?.topic || "Untitled Topic"}
          </h3>
        </div>

        <div className="flex shrink-0 items-center justify-between rounded-xl border border-violet-400/10 bg-violet-500/[0.05] px-4 py-3 sm:min-w-28 sm:flex-col sm:items-end sm:border-0 sm:bg-transparent sm:p-0">

          <p className="text-[10px] font-medium uppercase tracking-[0.12em] text-zinc-600">
            Demand Score
          </p>

          <p className="text-2xl font-semibold tracking-tight text-violet-400 sm:mt-1">
            {demandScore.toFixed(2)}
          </p>

        </div>
      </div>

      <div className="mt-6 grid grid-cols-3 gap-2 sm:gap-3">

        <Metric
          label="Requests"
          value={recommendation?.request_count ?? 0}
        />

        <Metric
          label="Likes"
          value={recommendation?.total_likes ?? 0}
        />

        <Metric
          label="Replies"
          value={recommendation?.total_replies ?? 0}
        />

      </div>

      {recommendation?.representative_comment && (
        <div className="mt-6 border-t border-white/[0.06] pt-5">

          <p className="text-[10px] font-medium uppercase tracking-[0.12em] text-zinc-600">
            Representative Audience Request
          </p>

          <blockquote className="mt-2 text-sm leading-6 text-zinc-400">
            "{recommendation.representative_comment}"
          </blockquote>

        </div>
      )}

    </article>
  );
}

function Metric({
  label,
  value,
}) {
  return (
    <div className="min-w-0 rounded-xl border border-white/[0.05] bg-[#11121a] px-3 py-3 sm:px-4">

      <p className="truncate text-[10px] uppercase tracking-[0.08em] text-zinc-600">
        {label}
      </p>

      <p className="mt-1 truncate text-base font-semibold text-zinc-200">
        {value}
      </p>

    </div>
  );
}

export default RecommendationCard;