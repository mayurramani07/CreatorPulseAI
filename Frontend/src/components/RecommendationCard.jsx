function RecommendationCard({
  rank,
  recommendation,
}) {
  return (
    <div className="recommendation-card">

      <div className="recommendation-top">

        <div>
          <span className="recommendation-rank">
            #{rank}
          </span>

          <h3 className="recommendation-topic">
            {recommendation.topic}
          </h3>
        </div>

        <div className="demand-score">
          <span>Demand Score</span>

          <strong>
            {recommendation.demand_score.toFixed(2)}
          </strong>
        </div>

      </div>


      <div className="recommendation-metrics">

        <div className="metric">
          <span>Requests</span>
          <strong>
            {recommendation.request_count}
          </strong>
        </div>


        <div className="metric">
          <span>Likes</span>
          <strong>
            {recommendation.total_likes}
          </strong>
        </div>


        <div className="metric">
          <span>Replies</span>
          <strong>
            {recommendation.total_replies}
          </strong>
        </div>

      </div>


      <div className="representative-comment">

        <span>
          Representative audience request
        </span>

        <p>
          "{recommendation.representative_comment}"
        </p>

      </div>

    </div>
  );
}

export default RecommendationCard;