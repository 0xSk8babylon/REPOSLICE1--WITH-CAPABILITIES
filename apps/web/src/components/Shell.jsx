export function Shell({ navigation, children }) {
  return (
    <div className="shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Residential Energy Planner</p>
          <h1>Persistent home energy design, not one-off proposals.</h1>
          <p className="hero-copy">
            Model the property, compare architectures, explain tradeoffs, and preserve expansion pathways over time.
          </p>
        </div>
        <div className="hero-card">
          <span>System philosophy</span>
          <strong>Structured facts and rules first. AI second.</strong>
        </div>
      </header>
      {navigation}
      <main className="content">{children}</main>
    </div>
  );
}

