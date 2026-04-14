"""Synthetic weather-like rows using Faker, aligned with preprocessed_weather.pkl schema."""

from __future__ import annotations

import pandas as pd
from faker import Faker


def preprocess_like_training_notebook(df: pd.DataFrame) -> pd.DataFrame:
    """Match the first preprocessing block in notebooks/training.ipynb."""
    out = df.copy()
    out["time"] = pd.to_datetime(out["time"])
    out["year"] = out["time"].dt.year
    out["month"] = out["time"].dt.month
    out["day"] = out["time"].dt.day
    out = out.drop(columns=["time"])
    return pd.get_dummies(out, columns=["weather_code"], drop_first=True)


def align_feature_columns(X: pd.DataFrame, reference_columns: pd.Index) -> pd.DataFrame:
    """Reindex so one-hot columns match the training frame (missing dummies become 0)."""
    return X.reindex(columns=reference_columns, fill_value=0)


def generate_fake_weather(template: pd.DataFrame, n_rows: int, seed: int = 42) -> pd.DataFrame:
    """
    Build a DataFrame with the same columns as the preprocessed pickle (before training transforms).

    Dates use Faker's ``date_between`` in the template's time range. Numeric fields use
    ``pyfloat`` / ``pyint`` within per-column min/max of ``template`` so scales resemble
    real data. ``weather_code`` is sampled uniformly from observed categories.
    """
    fake = Faker()
    fake.seed_instance(seed)

    template = template.copy()
    template["time"] = pd.to_datetime(template["time"])
    wc = template["weather_code"]
    codes = wc.cat.categories.tolist() if hasattr(wc, "cat") else sorted(wc.unique().tolist())

    t0 = template["time"].min().date()
    t1 = template["time"].max().date()

    feature_cols = [c for c in template.columns if c not in ("time", "weather_code")]
    bounds: dict[str, tuple[float, float]] = {}
    for c in feature_cols:
        lo = float(template[c].min())
        hi = float(template[c].max())
        if lo == hi:
            hi = lo + 1e-6
        bounds[c] = (lo, hi)

    rows: list[dict] = []
    for _ in range(n_rows):
        row: dict = {
            "time": pd.Timestamp(fake.date_between(start_date=t0, end_date=t1)),
            "weather_code": int(fake.random_element(elements=codes)),
        }
        for c in feature_cols:
            lo, hi = bounds[c]
            dtype = template[c].dtype
            if pd.api.types.is_integer_dtype(dtype):
                row[c] = int(round(fake.pyfloat(min_value=lo, max_value=hi, right_digits=6)))
            else:
                row[c] = float(fake.pyfloat(min_value=lo, max_value=hi, right_digits=6))
        rows.append(row)

    out = pd.DataFrame(rows)
    out["weather_code"] = pd.Categorical(out["weather_code"], categories=codes, ordered=False)

    for c in feature_cols:
        if pd.api.types.is_integer_dtype(template[c].dtype):
            out[c] = out[c].astype(template[c].dtype)
        else:
            out[c] = out[c].astype(template[c].dtype)

    return out.reindex(columns=template.columns)
