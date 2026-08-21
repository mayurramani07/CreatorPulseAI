function StatsCard({
  label,
  value,
  description,
}) {
  return (
    <div className="group rounded-2xl border border-white/[0.07] bg-white/[0.025] p-6 backdrop-blur-xl transition-all duration-300 hover:-translate-y-1 hover:border-violet-400/20 hover:bg-white/[0.04]">

      <p className="text-[11px] font-medium uppercase tracking-[0.12em] text-zinc-500">
        {label}
      </p>

      <p className="mt-3 text-3xl font-semibold tracking-tight text-zinc-100">
        {value}
      </p>

      <p className="mt-2 text-xs leading-5 text-zinc-600">
        {description}
      </p>

    </div>
  );
}

export default StatsCard;