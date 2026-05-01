# WeatherML

Weather prediction with **Jupyter notebooks**, Python **training utilities** under `src/weatherml`, and a **Vite + React** frontend backed by a **FastAPI** service in [`weatherml-web/`](weatherml-web/).

## Prerequisites

- **Python 3.12+** (UV can install it)
- **[UV](https://docs.astral.sh/uv/getting-started/installation/)** — package manager for the Python project
- **Node.js 18+** and **npm** — for the web UI (in `weatherml-web/`)

## Quick start

### 1. Clone and enter the repo

```bash
git clone <repo-url>
cd WeatherML
```

### 2. Python environment

Install runtime deps plus dev (lint, notebooks) and **web** (FastAPI, Uvicorn):

```bash
uv sync --group dev --group web
```

Notebook-only work is fine with `uv sync` alone; add `--group web` when you want to run the API from the repo root.

### 3. Web app (predictor UI)

The API searches **`notebooks/artifacts/`** recursively for **`model.pkl`** or **`best_model.pkl`** (e.g. `notebooks/artifacts/lgb_…/model.pkl` from a training run). If several exist, it loads the **most recently modified** file. Optional: set **`WEATHERML_MODEL_PATH`** to one exact file.

Copy **`feature_columns.json`** and **`weather_code_categories.json`** into that **same folder as the model** if you can; otherwise the API falls back to another copy under **`notebooks/artifacts/`** (newest) or **`weatherml-web/model/`**.

**Terminal A — API (port 8000):**

```bash
uv run --group web uvicorn main:app --reload --port 8000 --app-dir weatherml-web
```

**Terminal B — frontend (Vite, port 5173):**

```bash
cd weatherml-web
npm install
npm run dev
```

Open **http://127.0.0.1:5173**. The dev server proxies `/api` to the FastAPI process.

**Alternative — API dependencies only via pip:**

```bash
cd weatherml-web
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 4. Notebooks and training

```bash
uv run jupyter lab
uv run python scripts/train.py
```

`scripts/train.py` is a stub until you wire it to your pipeline; notebooks under `notebooks/` are the main experimentation path.

### Lint and format

```bash
uv run ruff check .
uv run ruff format .
```

## Dev container

Open the folder in **VS Code** or **Cursor** with [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers). The container runs `uv sync` on create/start. Forwarded ports:

- **5173** — Vite (`npm run dev` in `weatherml-web/`, requires Node locally or a Node feature added to the container)
- **8000** — FastAPI (`uv run --group web uvicorn …` as above)

Install Node in the container or run the frontend on your host while the API runs in the container.

## Optional: Weights & Biases

```bash
uv run wandb login
```

Use W&B from notebooks or once `scripts/train.py` supports logging.

## Project layout

```
├── notebooks/          # Experiments; artifacts/ holds exported .pkl (and optional JSON) for the API
├── scripts/          # CLI helpers (training stub, data scripts)
├── src/weatherml/    # Shared Python package (model helpers)
├── weatherml-web/    # FastAPI (main.py), Vite UI; committed JSON defaults under model/
├── data/             # Datasets (see .gitignore for large paths)
└── pyproject.toml    # Python deps; [dependency-groups] dev + web
```
