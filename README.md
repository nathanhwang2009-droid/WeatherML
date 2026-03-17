# WeatherML

ML project for weather prediction with Jupyter notebooks for experimentation and Python scripts for model training and a Streamlit dashboard.

## Prerequisites

- **Python 3.12+** (UV will install it if missing)
- **UV** – fast Python package manager ([install](https://docs.astral.sh/uv/getting-started/installation/))

## Quick Start (Partner Setup)

### 1. Install UV

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and Enter the Project

```bash
git clone <repo-url>
cd WeatherML
```

### 3. Create the Virtual Environment & Install Dependencies

UV creates the virtual environment (`.venv`) and installs all dependencies in one step:

```bash
uv sync
```

This will:
- Create `.venv` in the project root
- Install Python 3.12 if needed
- Install all dependencies from `pyproject.toml`
- Generate `uv.lock` if missing

### 4. Verify Setup

```bash
# Run the Streamlit dashboard
uv run streamlit run scripts/dashboard.py

# Or train the model
uv run python scripts/train.py
```

## Development Workflow

### Using the Dev Container (Recommended)

Open the project in **VS Code** or **Cursor** with the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension. The container will:

- Install UV and Python
- Run `uv sync` on create and start
- Forward port 8501 for Streamlit

### Automatic Tasks on Project Open

When opening the project in VS Code/Cursor, two tasks run automatically (if enabled):

1. **Git Pull** – fetches latest changes
2. **UV Sync** – updates dependencies

To enable: run **Tasks: Manage Automatic Tasks in Folder** (Cmd+Shift+P) → **Allow Automatic Tasks in Folder**.

### Running Commands

All commands use `uv run` so they run inside the project’s virtual environment:

```bash
uv run streamlit run scripts/dashboard.py   # Dashboard
uv run python scripts/train.py              # Train model
uv run jupyter lab                           # Jupyter Lab
uv run ruff check .                          # Lint
uv run ruff format .                         # Format
```

### Weights & Biases (Optional)

For experiment tracking, set up [W&B](https://wandb.ai/) and log in:

```bash
uv run wandb login
```

Then train with `--wandb`:

```bash
uv run python scripts/train.py --wandb
```

## Project Structure

```
├── notebooks/       # Jupyter notebooks for experimentation
├── scripts/         # Python scripts (training, dashboard)
├── src/             # Reusable Python modules
├── data/            # Raw and processed data
└── pyproject.toml   # Project config and dependencies
```
