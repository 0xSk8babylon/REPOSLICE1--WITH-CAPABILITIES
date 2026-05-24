export function FormField({ label, hint, children }) {
  return (
    <label className="form-field">
      <span className="form-label">{label}</span>
      {hint ? <small className="form-hint">{hint}</small> : null}
      {children}
    </label>
  );
}

