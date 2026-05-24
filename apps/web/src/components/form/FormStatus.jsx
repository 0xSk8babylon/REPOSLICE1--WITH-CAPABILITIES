export function FormStatus({ saving, error, successMessage }) {
  if (error) {
    return (
      <div className="form-status error">
        <strong>Save failed.</strong>
        <span>{error.message}</span>
      </div>
    );
  }

  if (saving) {
    return <div className="form-status">Saving changes...</div>;
  }

  if (successMessage) {
    return <div className="form-status success">{successMessage}</div>;
  }

  return null;
}
