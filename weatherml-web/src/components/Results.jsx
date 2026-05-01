export default function Results({ prediction }) {
  const formatted =
    typeof prediction === "number" && Number.isFinite(prediction)
      ? prediction.toLocaleString(undefined, { maximumFractionDigits: 4 })
      : String(prediction);

  return (
    <section className="mt-8 overflow-hidden rounded-2xl border border-emerald-500/25 bg-gradient-to-br from-emerald-950/50 to-surface-card shadow-glow">
      <div className="border-b border-emerald-500/15 bg-emerald-950/30 px-6 py-4">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-emerald-300/90">
          Model output
        </h2>
        <p className="mt-1 text-sm text-slate-400">
          Regression score from your trained model (e.g. under{" "}
          <span className="font-mono text-slate-300">notebooks/artifacts/</span>) — the
          same target column used when training (often a next-step weather measurement).
        </p>
      </div>
      <div className="px-6 py-8">
        <p className="font-mono text-4xl font-medium tabular-nums tracking-tight text-emerald-400 sm:text-5xl">
          {formatted}
        </p>
      </div>
    </section>
  );
}
