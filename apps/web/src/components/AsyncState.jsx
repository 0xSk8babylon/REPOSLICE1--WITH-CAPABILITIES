export function LoadingState({ label = "Loading data..." }) {
  return <div className="state-card">{label}</div>;
}

export function ErrorState({ error, label = "Unable to load data." }) {
  return (
    <div className="state-card error">
      <strong>{label}</strong>
      <span>{error?.message || "Unknown error"}</span>
    </div>
  );
}

export function EmptyState({ label = "No data available yet." }) {
  return <div className="state-card empty">{label}</div>;
}

