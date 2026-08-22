function formatNumber(value) {
  return new Intl.NumberFormat("en", {
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(value ?? 0);
}

function VideoInfo({ analysis }) {
  if (!analysis?.video) {
    return null;
  }

  const {
    title,
    channel_name,
    thumbnail_url,
    view_count,
    like_count,
    total_comments,
  } = analysis.video;

  return (
    <div className="mx-auto mt-10 w-full max-w-5xl px-5 sm:px-6 lg:px-8">
      <div className="overflow-hidden rounded-2xl border border-white/[0.07] bg-white/[0.025] backdrop-blur-xl">

        <div className="flex flex-col gap-6 p-5 sm:flex-row sm:p-6">

          {thumbnail_url && (
            <img
              src={thumbnail_url}
              alt={title || "YouTube video"}
              className="aspect-video w-full rounded-xl object-cover sm:w-64"
            />
          )}

          <div className="min-w-0 flex-1">

            <p className="text-[10px] font-medium uppercase tracking-[0.14em] text-violet-400/80">
              Analyzed Video
            </p>

            <h2 className="mt-2 line-clamp-2 text-lg font-semibold tracking-tight text-zinc-100 sm:text-xl">
              {title || "YouTube Video"}
            </h2>

            {channel_name && (
              <p className="mt-2 text-sm text-zinc-500">
                {channel_name}
              </p>
            )}

            <div className="mt-5 grid grid-cols-3 gap-2 sm:max-w-md sm:gap-3">

              <VideoMetric
                label="Views"
                value={formatNumber(view_count)}
              />

              <VideoMetric
                label="Likes"
                value={formatNumber(like_count)}
              />

              <VideoMetric
                label="Comments"
                value={formatNumber(total_comments)}
              />

            </div>

            <div className="mt-4 inline-flex items-center gap-2 rounded-lg border border-emerald-400/10 bg-emerald-500/[0.04] px-3 py-2">

              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />

              <span className="text-xs text-emerald-400/70">
                Analysis complete
              </span>

            </div>

          </div>

        </div>

      </div>
    </div>
  );
}

function VideoMetric({ label, value }) {
  return (
    <div className="rounded-xl border border-white/[0.05] bg-[#11121a] px-3 py-3">
      <p className="text-[10px] uppercase tracking-[0.08em] text-zinc-600">
        {label}
      </p>

      <p className="mt-1 text-sm font-semibold text-zinc-200 sm:text-base">
        {value}
      </p>
    </div>
  );
}

export default VideoInfo;