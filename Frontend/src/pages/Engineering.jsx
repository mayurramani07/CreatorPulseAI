import Architecture from "../components/engineering/Architecture";

function Engineering() {
  return (
    <main className="min-h-screen bg-[#08090d] px-6 pb-24 pt-32 text-white lg:px-8">
      <div className="mx-auto w-full max-w-7xl">

        <div className="max-w-3xl">
          <p className="text-xs font-medium uppercase tracking-[0.14em] text-violet-400/80">
            Engineering
          </p>

          <h1 className="mt-4 text-4xl font-semibold tracking-tight text-zinc-100 sm:text-5xl lg:text-6xl">
            How CreatorPulseAI is engineered.
          </h1>

          <p className="mt-6 max-w-2xl text-sm leading-7 text-zinc-500 sm:text-base">
            Explore the architecture, AI pipeline, infrastructure,
            scalability decisions, and reliability mechanisms
            behind CreatorPulseAI.
          </p>
        </div>

        <Architecture />

      </div>
    </main>
  );
}

export default Engineering;