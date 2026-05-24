import { useEffect, useState } from "react";

export function useApiQuery(queryKey, queryFn, options = {}) {
  const { enabled = true, initialData = null } = options;
  const [data, setData] = useState(initialData);
  const [loading, setLoading] = useState(enabled);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!enabled) {
      setLoading(false);
      return undefined;
    }

    let cancelled = false;

    async function run() {
      setLoading(true);
      setError(null);

      try {
        const result = await queryFn();
        if (!cancelled) {
          setData(result);
        }
      } catch (queryError) {
        if (!cancelled) {
          setError(queryError);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    run();

    return () => {
      cancelled = true;
    };
  }, [enabled, queryKey]);

  return { data, loading, error };
}
