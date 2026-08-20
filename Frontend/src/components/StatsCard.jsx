function StatsCard({
  label,
  value,
  description,
}) {
  return (
    <div className="stats-card">
      <p className="stats-label">
        {label}
      </p>

      <h3 className="stats-value">
        {value}
      </h3>

      {description && (
        <p className="stats-description">
          {description}
        </p>
      )}
    </div>
  );
}

export default StatsCard;