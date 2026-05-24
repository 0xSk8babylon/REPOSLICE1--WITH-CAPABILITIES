export function ScoreCard({ label, value, detail }) {
  return (
    <article className="score-card">
      <span>{label}</span>
      <strong>{value}</strong>
      {detail ? <p>{detail}</p> : null}
    </article>
  );
}

