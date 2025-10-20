# ✈️ Ryanair Fuel Risk Analyzer


## 🧠 Overview
A **Python-based data pipeline** analyzing **Ryanair’s stock performance (1997–2025)** versus **global jet fuel price trends**.  
It identifies high-fuel-risk months that trigger negative returns and produces **forecast-ready datasets** for visualization or ML modeling.

This project merges financial data, performs scenario analysis, and exports insights used for dashboards or forecasting tools.

---

## Key Highlights
- **200+ months of data** — auto-merged & cleaned from raw CSV/XLS files.  
- **15 “red-alert” months** — when fuel >20% above average, stock returns drop by ~8%.  
- **Hybrid forecasting** (ARIMA + Random Forest, via external model) projects Ryanair stock near **€36–40 for 2025–26**.  
- Outputs are **Power BI-ready** (scenario CSV + forecast CSV + SQLite DB).  
- **Fully automated ETL** — from raw data ingestion to insight export.

---

## 🛠️ Tech Stack
- **Languages:** Python 3, SQL  
- **Libraries:** Pandas | NumPy | SQLite3 | Statsmodels | Scikit-Learn  
- **Data Sources:**  
  - `ryanair_stock.csv` – daily stock data (MacroTrends)  
  - `jet_fuel_prices.xls` – weekly global fuel prices (EIA)  

---

## 📂 File Structure
| File | Description |
|------|-------------|
| `main.py` | ETL script — loads raw stock & fuel data, merges monthly, saves to SQLite DB |
| `run_scenarios.py` | Runs SQL queries for insights & exports `scenario_fuel.csv` |
| `forecast_models.ipynb` | Optional notebook for forecasting visualizations |
| `forecast_results.csv` | ARIMA / RF / Combined forecast results (2021–2025) |
| `scenario_fuel.csv` | High-fuel-risk months (15 worst spikes) |
| `ryanair_data.db` | SQLite database containing cleaned monthly data |
| `jet_fuel_prices.xls` | Raw fuel price data |
| `ryanair_stock.csv` | Raw stock data |


---

