export function PageSection({ title, description, children }) {
  return (
    <section className="page-section">
      <div className="section-heading">
        <h2>{title}</h2>
        {description ? <p>{description}</p> : null}
      </div>
      {children}
    </section>
  );
}

