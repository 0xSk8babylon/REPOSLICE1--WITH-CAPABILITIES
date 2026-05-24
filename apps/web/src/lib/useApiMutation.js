import { useState } from "react";

export function useApiMutation() {
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  async function run(action) {
    setSaving(true);
    setError(null);

    try {
      return await action();
    } catch (mutationError) {
      setError(mutationError);
      throw mutationError;
    } finally {
      setSaving(false);
    }
  }

  function clearError() {
    setError(null);
  }

  return { saving, error, run, clearError };
}

