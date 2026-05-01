import { useEffect, useState } from "react";
import PredictionForm from "./components/PredictionForm";
import Results from "./components/Results";

function formatDetail(detail) {
  if (detail == null) return "Something went wrong";
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((d) =>
        typeof d === "object" && d.msg ? `${d.loc?.join(".")}: ${d.msg}` : JSON.stringify(d),
      )
      .join(" ");
  }
  return String(detail);
}

async function readErrorMessage(res) {
  try {
    const data = await res.json();
    return formatDetail(data.detail) || res.statusText;
  } catch {
    return res.statusText || "Request failed";
  }
}

function App() {
  const [metadata, setMetadata] = useState({ weather_codes: [], numeric_features: [] });
  const [metaLoading, setMetaLoading] = useState(true);
  const [metaError, setMetaError] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setMetaLoading(true);
      setMetaError(null);
      try {
        const res = await fetch("/api/metadata");
        if (!res.ok) throw new Error(await readErrorMessage(res));
        const data = await res.json();
        if (!cancelled) setMetadata(data);
      } catch (e) {
        if (!cancelled) setMetaError(e.message || "Failed to load metadata");
      } finally {
        if (!cancelled) setMetaLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const handlePredict = async (formData) => {
    setLoading(true);
    setError(null);
    setPrediction(null);
    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(formatDetail(data.detail));
      setPrediction(data.prediction);
    } catch (err) {
      setError(err.message || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  const formDisabled = metaLoading || !!metaError || metadata.numeric_features.length === 0;

  return (
    <div className="min-h-screen pb-20 pt-10 px-4 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-3xl">
        <header className="mb-10 text-center">
          <p className="mb-2 text-xs font-semibold uppercase tracking-[0.22em] text-accent">
            WeatherML
          </p>
          <h1 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Weather prediction
          </h1>
          <p className="mx-auto mt-3 max-w-lg text-sm leading-relaxed text-surface-muted">
            Enter a date, weather code, and the observed measurements below. The trained model returns a
            single regression score (your project&apos;s target from training, e.g. a temperature-derived
            quantity).
          </p>
        </header>

        {metaError && (
          <div
            className="mb-8 rounded-xl border border-red-500/30 bg-red-950/40 px-4 py-3 text-sm text-red-200 shadow-card"
            role="alert"
          >
            <p className="font-medium">Could not load the API</p>
            <p className="mt-1 text-red-300/90">{metaError}</p>
            <p className="mt-2 text-xs text-red-400/80">
              Start the API:{" "}
              <code className="rounded bg-black/30 px-1.5 py-0.5 font-mono text-[11px]">
                uvicorn main:app --reload --port 8000
              </code>{" "}
              from the <code className="font-mono text-[11px]">weatherml-web</code> directory.
            </p>
          </div>
        )}

        {metaLoading && (
          <div className="mb-8 flex items-center justify-center gap-3 rounded-2xl border border-slate-700/50 bg-surface-card/80 py-10 shadow-card">
            <span
              className="h-5 w-5 animate-spin rounded-full border-2 border-accent border-t-transparent"
              aria-hidden
            />
            <span className="text-sm text-surface-muted">Loading form metadata…</span>
          </div>
        )}

        {!metaLoading && !metaError && (
          <>
            <PredictionForm
              metadata={metadata}
              onSubmit={handlePredict}
              loading={loading}
              disabled={formDisabled}
            />
            {prediction !== null && !loading && <Results prediction={prediction} />}
          </>
        )}

        {error && (
          <div
            className="mt-6 rounded-xl border border-amber-500/35 bg-amber-950/35 px-4 py-3 text-sm text-amber-100 shadow-card"
            role="alert"
          >
            {error}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
