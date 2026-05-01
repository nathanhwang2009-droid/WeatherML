"""FastAPI server for WeatherML predictions."""

from __future__ import annotations

import json
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated, Any

import joblib
import numpy as np
import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field, field_validator

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
ARTIFACTS_DIR = REPO_ROOT / "notebooks" / "artifacts"
WEB_MODEL_DIR = BASE_DIR / "model"


def _gather_artifact_pickles() -> list[Path]:
    """All model.pkl / best_model.pkl under notebooks/artifacts (any depth)."""
    if not ARTIFACTS_DIR.is_dir():
        return []
    found: dict[Path, Path] = {}
    for pattern in ("best_model.pkl", "model.pkl", "**/best_model.pkl", "**/model.pkl"):
        for p in ARTIFACTS_DIR.glob(pattern):
            if p.is_file():
                found[p.resolve()] = p
    out = list(found.values())
    out.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    return out


def resolve_model_path() -> Path:
    """Prefer notebooks/artifacts (nested run dirs from training); optional WEATHERML_MODEL_PATH."""
    raw = os.environ.get("WEATHERML_MODEL_PATH")
    if raw:
        p = Path(raw).expanduser().resolve()
        if not p.is_file():
            msg = f"WEATHERML_MODEL_PATH is not a file: {p}"
            raise FileNotFoundError(msg)
        return p
    candidates = _gather_artifact_pickles()
    if candidates:
        return candidates[0]
    legacy = WEB_MODEL_DIR / "best_model.pkl"
    if legacy.is_file():
        return legacy
    msg = (
        "No model file found. Expected model.pkl or best_model.pkl under notebooks/artifacts/ "
        "(including subfolders from training runs), set WEATHERML_MODEL_PATH, or place "
        f"best_model.pkl under weatherml-web/model/. Searched: {ARTIFACTS_DIR}"
    )
    raise FileNotFoundError(msg)


def _gather_artifact_json(filename: str) -> list[Path]:
    if not ARTIFACTS_DIR.is_dir():
        return []
    found: dict[Path, Path] = {}
    for p in (ARTIFACTS_DIR / filename, *ARTIFACTS_DIR.glob(f"**/{filename}")):
        if p.is_file():
            found[p.resolve()] = p
    out = list(found.values())
    out.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    return out


def resolve_sidecar_json(filename: str) -> Path:
    """JSON next to training runs under artifacts (any depth), else weatherml-web/model/."""
    matches = _gather_artifact_json(filename)
    if matches:
        return matches[0]
    fallback = WEB_MODEL_DIR / filename
    if fallback.is_file():
        return fallback
    msg = f"Missing {filename}. Add it under {ARTIFACTS_DIR} (optionally in a run subfolder) or {WEB_MODEL_DIR}"
    raise FileNotFoundError(msg)


def _booster_feature_names(model: Any) -> list[str] | None:
    booster = getattr(model, "booster_", None)
    if booster is None:
        return None
    try:
        names = booster.feature_name()
    except Exception:
        return None
    if not names or not all(names):
        return None
    return list(names)


def _resolve_model_input_columns(
    model: Any,
    feature_columns: list[str],
    inference_columns: list[str],
) -> list[str]:
    """Column order/count expected at predict time (training may have included ``target`` in X)."""
    names = getattr(model, "feature_names_in_", None)
    if names is not None and len(names) > 0:
        return list(names)
    bnames = _booster_feature_names(model)
    if bnames is not None:
        return bnames
    n = getattr(model, "n_features_in_", None)
    if n is None:
        return list(feature_columns)
    if len(feature_columns) == n:
        return list(feature_columns)
    if len(inference_columns) == n:
        return list(inference_columns)
    return list(feature_columns)


class AppState:
    model: Any
    weather_codes: list
    numeric_features: list[str]
    inference_columns: list[str]
    model_input_columns: list[str]


@asynccontextmanager
async def lifespan(app: FastAPI):
    state = AppState()
    model_path = resolve_model_path()
    model_dir = model_path.parent

    def sidecar(filename: str) -> Path:
        p = model_dir / filename
        if p.is_file():
            return p
        return resolve_sidecar_json(filename)

    feature_path = sidecar("feature_columns.json")
    weather_path = sidecar("weather_code_categories.json")
    with feature_path.open(encoding="utf-8") as f:
        feature_columns: list[str] = json.load(f)
    state.inference_columns = [c for c in feature_columns if c != "target"]
    state.numeric_features = [
        col
        for col in state.inference_columns
        if col not in {"year", "month", "day"} and not col.startswith("weather_code_")
    ]
    with weather_path.open(encoding="utf-8") as f:
        state.weather_codes = json.load(f)
    state.model = joblib.load(model_path)
    state.model_input_columns = _resolve_model_input_columns(
        state.model,
        feature_columns,
        state.inference_columns,
    )
    app.state.weatherml = state
    yield


app = FastAPI(title="WeatherML API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_state(request: Request) -> AppState:
    return request.app.state.weatherml


def preprocess_payload(state: AppState, payload: dict) -> pd.DataFrame:
    date_value = payload.get("date", "")
    if not date_value:
        raise ValueError("Date is required.")

    dt = pd.to_datetime(date_value)
    row: dict[str, Any] = {
        "year": int(dt.year),
        "month": int(dt.month),
        "day": int(dt.day),
        "weather_code": payload.get("weather_code"),
    }

    for feature in state.numeric_features:
        value = payload.get(feature, "")
        row[feature] = float(value) if value != "" and value is not None else 0.0

    df = pd.DataFrame([row])
    df = pd.get_dummies(df, columns=["weather_code"], drop_first=True)
    df = df.reindex(columns=state.model_input_columns, fill_value=0)
    return df.astype(np.float64)


class PredictRequest(BaseModel):
    date: str = Field(..., min_length=1)
    weather_code: int
    model_config = ConfigDict(extra="allow")

    @field_validator("date")
    @classmethod
    def date_non_empty(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("Date is required.")
        return v


@app.get("/api/metadata")
def metadata(state: Annotated[AppState, Depends(get_state)]):
    return {
        "weather_codes": state.weather_codes,
        "numeric_features": state.numeric_features,
    }


@app.post("/api/predict")
def predict(
    body: PredictRequest,
    state: Annotated[AppState, Depends(get_state)],
):
    payload = body.model_dump()
    try:
        x = preprocess_payload(state, payload)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    try:
        prediction = state.model.predict(x)[0]
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Model prediction failed: {e!s}",
        ) from e
    return {"prediction": float(prediction)}
