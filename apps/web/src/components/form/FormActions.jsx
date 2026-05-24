export function FormActions({ saving, onCancel, saveLabel = "Save", cancelLabel = "Cancel" }) {
  return (
    <div className="form-actions">
      <button className="button button-primary" type="submit" disabled={saving}>
        {saving ? "Saving..." : saveLabel}
      </button>
      {onCancel ? (
        <button className="button button-secondary" type="button" onClick={onCancel} disabled={saving}>
          {cancelLabel}
        </button>
      ) : null}
    </div>
  );
}

