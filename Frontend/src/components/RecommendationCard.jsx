function RecommendationCard({
  recommendation,
  rank,
}) {
  return (
    <article className="group rounded-2xl border border-white/[0.07] bg-white/[0.025] p-6 backdrop-blur-xl transition-all duration-300 hover:-translate-y-1 hover:border-violet-400/20 hover:bg-white/[0.04]">

      {/* Top Section */}

      <div className="flex items-start justify-between gap-6">

        <div className="min-w-0">

          <p className="text-[11px] font-medium uppercase tracking-[0.12em] text-zinc-600">
            #{String(rank).padStart(2, "0")}
          </p>

          <h3 className="mt-2 text-xl font-semibold tracking-tight text-zinc-100">
            {recommendation.topic}
          </h3>

        </div>


        {/* Demand Score */}

        <div className="shrink-0 text-right">

          <p className="text-[10px] font-medium uppercase tracking-[0.12em] text-zinc-600">
            Demand Score
          </p>

          <p className="mt-1 text-2xl font-semibold tracking-tight text-violet-400">
            {Number(
              recommendation.demand_score
            ).toFixed(2)}
          </p>

        </div>

      </div>


      {/* Metrics */}

      <div className="mt-6 grid grid-cols-3 gap-2 sm:flex sm:gap-3">

        <Metric
          label="Requests"
          value={recommendation.request_count}
        />

        <Metric
          label="Likes"
          value={recommendation.total_likes}
        />

        <Metric
          label="Replies"
          value={recommendation.total_replies}
        />

      </div>


      {/* Representative Comment */}

      {recommendation.representative_comment && (
        <div className="mt-6 border-t border-white/[0.06] pt-5">

          <p className="text-[10px] font-medium uppercase tracking-[0.12em] text-zinc-600">
            Representative Audience Request
          </p>

          <p className="mt-2 text-sm leading-6 text-zinc-400">
            "{recommendation.representative_comment}"
          </p>

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
    <div className="min-w-0 flex-1 rounded-xl border border-white/[0.05] bg-[#11121a] px-3 py-3">

      <p className="text-[10px] uppercase tracking-[0.08em] text-zinc-600">
        {label}
      </p>

      <p className="mt-1 text-base font-semibold text-zinc-200">
        {value}
      </p>

    </div>
  );
}


export default RecommendationCard;