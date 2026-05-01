import { useEffect, useMemo, useState } from "react";

function labelize(name) {
  return name.replace(/_/g, " ");
}

export default function PredictionForm({ metadata, onSubmit, loading, disabled }) {
  const defaults = useMemo(
    () => ({
      date: "",
      weather_code: metadata.weather_codes[0] ?? 0,
      ...Object.fromEntries((metadata.numeric_features || []).map((f) => [f, "0"])),
    }),
    [metadata],
  );

  const [formData, setFormData] = useState(defaults);
  const [fieldError, setFieldError] = useState("");

  useEffect(() => {
    setFormData(defaults);
  }, [defaults]);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFieldError("");
    setFormData((prev) => ({
      ...prev,
      [name]: type === "number" ? value : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.date?.trim()) {
      setFieldError("Choose a date to continue.");
      return;
    }
    const payload = {
      date: formData.date,
      weather_code:
        typeof formData.weather_code === "number"
          ? formData.weather_code
          : Number(formData.weather_code),
    };
    for (const feature of metadata.numeric_features) {
      const raw = formData[feature];
      payload[feature] = raw === "" || raw == null ? 0 : Number(raw);
    }
    onSubmit(payload);
  };

  const inputClass =
    "mt-1.5 w-full rounded-lg border border-slate-600/60 bg-surface-elevated px-3 py-2.5 text-sm text-white placeholder-slate-500 shadow-inner outline-none transition focus:border-accent focus:ring-1 focus:ring-accent/40";

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-2xl border border-slate-700/50 bg-surface-card/90 p-6 shadow-card sm:p-8"
    >
      <h2 className="text-lg font-semibold text-white">Inputs</h2>
      <p className="mt-1 text-sm text-surface-muted">
        Values are sent to the model in the same shape as training (minus the label column &quot;target&quot;).
      </p>

      {fieldError && (
        <p className="mt-4 rounded-lg border border-red-500/40 bg-red-950/30 px-3 py-2 text-sm text-red-200">
          {fieldError}
        </p>
      )}

      <div className="mt-6 grid gap-6 sm:grid-cols-2">
        <label className="block text-sm font-medium text-slate-300">
          Date
          <input
            type="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            disabled={disabled}
            required
            className={inputClass}
          />
        </label>

        <label className="block text-sm font-medium text-slate-300">
          Weather code
          <select
            name="weather_code"
            value={formData.weather_code}
            onChange={handleChange}
            disabled={disabled}
            className={`${inputClass} cursor-pointer appearance-none bg-[length:1rem] bg-[right_0.75rem_center] bg-no-repeat pr-10`}
            style={{
              backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2394a3b8'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E")`,
            }}
          >
            {metadata.weather_codes.map((code) => (
              <option key={code} value={code}>
                {code}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="mt-8">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">
          Numeric features
        </h3>
        <div className="mt-4 grid max-h-[min(55vh,28rem)] grid-cols-1 gap-4 overflow-y-auto pr-1 sm:grid-cols-2">
          {metadata.numeric_features.map((feature) => (
            <label key={feature} className="block text-sm font-medium text-slate-300">
              <span className="capitalize">{labelize(feature)}</span>
              <input
                type="number"
                step="any"
                name={feature}
                value={formData[feature] ?? "0"}
                onChange={handleChange}
                disabled={disabled}
                className={inputClass}
              />
            </label>
          ))}
        </div>
      </div>

      <div className="mt-8 flex flex-col items-stretch gap-3 sm:flex-row sm:justify-end">
        <button
          type="submit"
          disabled={disabled || loading}
          className="inline-flex items-center justify-center rounded-xl bg-accent px-6 py-3 text-sm font-semibold text-surface shadow-glow transition hover:bg-sky-300 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? (
            <>
              <span
                className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-surface border-t-transparent"
                aria-hidden
              />
              Running model…
            </>
          ) : (
            "Run prediction"
          )}
        </button>
      </div>
    </form>
  );
}
