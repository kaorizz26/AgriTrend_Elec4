# AgriTrend — Agricultural Commodity Price Forecasting

AgriTrend is an academic Python project that analyzes **Philippine monthly agricultural farmgate prices** from **PSA OpenSTAT** and forecasts the next **six months** for each selected commodity.

**Current scope:** data preparation, data cleaning, time-series model experiments, evaluation, and six-month forecasting. The Streamlit dashboard is **not implemented yet**. `app.py` is currently an empty placeholder.

## What the system does

1. Reads seven PSA OpenSTAT CSV datasets.
2. Transforms the monthly data into a consistent table and cleans the price records.
3. Tests three forecasting methods: **Seasonal Naïve**, **Holt-Winters**, and **AutoARIMA**.
4. Compares methods using six-month backtesting windows and **MAE/RMSE**.
5. Selects the lowest-MAE model (RMSE breaks ties) for each commodity and produces six monthly forecasts.

The saved project datasets contain **58 commodities** across **seven categories**, **174 model-comparison rows** (three models per commodity), and **348 forecast rows** (six months per commodity). These saved results can be used without rerunning the full model experiments.

## Requirements

- Windows 11 or a compatible desktop environment
- **Python 3.13** (used in the original project environment)
- Git
- Visual Studio Code with the **Python** and **Jupyter** extensions

> `requirements.txt` contains the packages and versions captured from the development environment, including pandas, numpy, matplotlib, scikit-learn, sktime, Jupyter, and forecasting dependencies. Installing these exact versions is easiest with a similar Python and operating-system environment.

## 1. Clone the repository

Open a VS Code terminal (PowerShell on Windows):

```powershell
git clone https://github.com/kaorizz26/AgriTrend_Elec4.git
cd AgriTrend_Elec4
```

Or use VS Code: **Source Control → Clone Repository**, paste the GitHub URL, and open the downloaded folder.

## 2. Create a virtual environment

Run from the **project root** (`AgriTrend_Elec4`):

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If `py -3.13` is unavailable but Python 3.13 is installed and selected, use `python -m venv .venv` instead. On PowerShell, if activation is blocked by the execution policy, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again.

## 3. Install dependencies

With `(.venv)` visible in the terminal:

```powershell
python -m pip install -r requirements.txt
```

The first installation may take some time. If a pinned package fails to install, share the exact error with the group rather than changing `requirements.txt` without coordination.

## 4. Open and run the notebooks

In VS Code, open a notebook from the `notebooks/` folder. Click **Select Kernel** at the upper right and choose the Python interpreter inside **`.venv`**.

| Order | Notebook | Purpose |
|---|---|---|
| 1 | `notebooks/01_data_preprocessing.ipynb` | Explore and combine PSA CSV data |
| 2 | `notebooks/02_data_cleaning.ipynb` | Clean and validate the combined dataset |
| 3 | `notebooks/03_single_commodity_demo.ipynb` | Demonstrate model comparison and six-month forecasting using one commodity |
| 4 | `notebooks/04_all_commodities_demo.ipynb` | Review evaluation and forecast results for all commodities |

**For a quick project walkthrough:** start with notebooks **03** and **04**. The necessary processed CSV files are already included in the repository. You do **not** need to rerun notebooks 01 and 02 just to view model results.

**Path reminder:** The notebook code uses relative paths such as `../data/processed/...`; run the notebooks in the `notebooks/` directory and avoid changing the working directory unexpectedly.

### Avoid unnecessary retraining

- Notebook 04 sets `run_full_evaluation = False` to **load the saved** `data/processed/model_evaluation_results.csv`. Keep it `False` for a normal demo. Setting it to `True` launches the full set of backtests.
- **Notebook 04 currently contains two separate cells labeled “Step 8.”** One always trains models for all commodities; the other **loads existing forecasts** from `data/processed/future_six_month_forecasts.csv` when available. **Skip the first Step 8 cell** during a quick demo, and run the second Step 8 cell instead.
- Notebook 03 includes an optional experiment that saves a fitted Palay model to `models/`. That folder is excluded from Git; it does not need to be committed.

## Project files

```text
AgriTrend_Elec4/
├── data/
│   ├── raw/             # Seven original PSA OpenSTAT CSV exports
│   └── processed/       # Cleaned prices, model results, and forecasts
├── notebooks/
│   ├── 01_data_preprocessing.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_single_commodity_demo.ipynb
│   ├── 04_all_commodities_demo.ipynb
│   ├── draft_01_model_implementation.ipynb
│   └── draft_02_forecasting_pipeline.ipynb
├── src/
│   ├── forecasting.py    # Models, training, forecasting helpers
│   └── evaluation.py     # Splitting, backtesting, model selection metrics
├── app.py                # Placeholder; not a working dashboard
├── requirements.txt
└── .gitignore
```

The `draft_*.ipynb` notebooks are **development references**, not the recommended demo notebooks.

### Important CSV outputs

| Path | Purpose |
|---|---|
| `data/processed/cleaned_farmgate_prices.csv` | Main cleaned monthly price history |
| `data/processed/model_evaluation_results.csv` | Model accuracy results for all commodities |
| `data/processed/best_models.csv` | Selected best model for each commodity |
| `data/processed/future_six_month_forecasts.csv` | Forecasted prices for the next six months |

## Working together on GitHub

Before starting work, open the project folder in the terminal and run:

```powershell
git pull origin main
```

For your own changes, use a separate branch when possible:

```powershell
git switch -c feature/your-task-name
# Edit the project files.
git add .
git commit -m "Describe your changes"
git push -u origin feature/your-task-name
```

Then open a **pull request** on GitHub so group members can review the change before merging it into `main`.

**Do not commit:** `.venv/`, private credentials, or generated model files. Avoid replacing saved evaluation/forecast CSV files during a demo without agreement.

## Troubleshooting

- **`ModuleNotFoundError`**: Verify the notebook kernel uses `.venv` and dependencies were installed there.
- **`FileNotFoundError: ../data/...`**: Check that the full repository was cloned and notebook execution is using the expected directory.
- **Notebook 04 takes a long time**: Keep `run_full_evaluation = False` and skip the first Step 8 cell, which always retrains models.
- **Permission denied when pushing**: Ask the repository owner for collaborator access, or create a fork and submit a pull request.

## Team study material

The **AgriTrend Complete Code & System Study Guide** explains the notebooks and reusable Python functions, with code walkthroughs, outputs, and defense questions. This guide can be added later under `docs/`.

## Data source

Philippine Statistics Authority (PSA), **OpenSTAT**, monthly farmgate price series: https://openstat.psa.gov.ph/
