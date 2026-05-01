# WeatherML web app

**FastAPI** inference API and **Vite + React** UI for the trained weather model.

## Run locally

**Model:** searches `notebooks/artifacts/` recursively for `model.pkl` or `best_model.pkl` (e.g. run folders like `lgb_lr0.01_…/model.pkl`). If several exist, the newest file wins. Set **`WEATHERML_MODEL_PATH`** to force one path.

**Metadata:** JSON in the **same folder as the chosen model**, else newest under `notebooks/artifacts/`, else `weatherml-web/model/`.

### API (port 8000)

From **repo root** (with `uv sync --group web`):

```bash
uv run --group web uvicorn main:app --reload --port 8000 --app-dir weatherml-web
```

Or from this directory after `pip install -r requirements.txt`:

```bash
uvicorn main:app --reload --port 8000
```

Endpoints:

- `GET /api/metadata` — weather code list and numeric feature names for the form
- `POST /api/predict` — JSON body with `date`, `weather_code`, and all numeric features (label column `target` is **not** sent; it is excluded from inference)

### Frontend (port 5173)

```bash
npm install
npm run dev
```

Vite proxies `/api` to `http://127.0.0.1:8000`. Open http://127.0.0.1:5173 .

### Production build

```bash
npm run build
```

Static output is in `dist/`. Serve with your own static host or extend FastAPI with `StaticFiles` if you want a single process.
