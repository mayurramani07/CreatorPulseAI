import StatsCard from "./StatsCard";
import RecommendationCard from "./RecommendationCard";

function AnalysisSection({ analysis }) {
  return (
    <section
      id="insights"
      className="mx-auto w-full max-w-7xl px-6 pb-24 lg:px-8"
    >

      <div className="mx-auto max-w-2xl text-center">

        <p className="text-xs font-medium uppercase tracking-[0.14em] text-violet-400/80">
          Audience Intelligence
        </p>

        <h2 className="mt-3 text-3xl font-semibold tracking-tight text-zinc-100 sm:text-4xl">
          Understand your audience.
        </h2>

        <p className="mt-4 text-sm leading-6 text-zinc-500">
          Here's what your audience is asking for.
        </p>

      </div>

      <div className="mt-10 grid grid-cols-1 gap-4 md:grid-cols-3">

        <StatsCard
          label="Comments Analyzed"
          value={analysis.processed_comments}
          description="Comments processed by CreatorPulse"
        />

        <StatsCard
          label="Content Requests"
          value={analysis.content_request_candidates}
          description="Audience requests detected"
        />

        <StatsCard
          label="Topics Identified"
          value={analysis.topic_groups}
          description="Distinct content opportunities"
        />

      </div>

      <div
        id="about"
        className="mt-20"
      >

        <div className="mb-7">

          <p className="text-xs font-medium uppercase tracking-[0.14em] text-violet-400/80">
            Content Opportunities
          </p>

          <h2 className="mt-2 text-2xl font-semibold tracking-tight text-zinc-100 sm:text-3xl">
            What your audience wants
          </h2>

          <p className="mt-2 text-sm text-zinc-500">
            Ranked by audience demand.
          </p>

        </div>

        <div className="flex flex-col gap-4">

          {analysis.recommendations?.map(
            (recommendation, index) => (
              <RecommendationCard
                key={`${recommendation.topic}-${index}`}
                recommendation={recommendation}
                rank={index + 1}
              />
            )
          )}

        </div>

      </div>

    </section>
  );
}

export default AnalysisSection;