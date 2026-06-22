# Stiesdal CDR Market Dashboard

An interactive dashboard for exploring the **Carbon Dioxide Removal (CDR) certificate market** — purchases, deliveries, suppliers, purchasers, and prices across CDR methods such as biochar, enhanced weathering, and direct air capture.

Built for [Stiesdal](https://www.stiesdal.com/) to track market activity in the voluntary CDR space, the dashboard turns the public [cdr.fyi](https://www.cdr.fyi/) transaction data into a filterable, at-a-glance view of who is buying and supplying carbon removal, at what volume, and at what price.

**Original demo:** https://stiesdal-cdr-dashboard.onrender.com/

> ⚠️ **The live demo is no longer functional.** The dashboard read its data live from a public [cdr.fyi](https://www.cdr.fyi/) Google Sheet. That feed has since been gated — the public export is now a frozen snapshot (data through Dec 31, 2023) with a different layout — so the app can no longer load it. This repository is preserved as a portfolio reference documenting how the dashboard was built.

---

## Features

- **Headline KPIs** — total tons purchased and delivered, share of purchases delivered, number of suppliers and purchasers, and average price per ton.
- **Method filter** — focus on a single CDR method (e.g. Biochar, Enhanced weathering) or view all methods together.
- **Date range selector** — free date range plus one-click presets (whole range, last year, last 30 days).
- **Top suppliers & purchasers** — ranked bar charts of the ten largest players by tons purchased/sold.
- **Price over time** — price-per-ton trend, split by method when viewing all methods.
- **Method share** — pie chart of how purchase volume is distributed across CDR methods.

All charts react instantly to the active method and date-range filters.

## Tech stack

- **[Dash](https://dash.plotly.com/)** (Flask + React) for the web app and reactive callbacks
- **[Plotly](https://plotly.com/python/)** for the interactive charts
- **pandas** / **NumPy** for data wrangling
- **Dash Bootstrap Components** for layout/styling
- **Gunicorn** + **Render** for production hosting

## Data source

The dashboard read its data live from a Google Sheet that mirrored and curated [cdr.fyi](https://www.cdr.fyi/) market transactions. On each app start, `src/components/_01_import_cdr.py` pulled the sheet via its public CSV export endpoint and derived fields such as price per ton — no credentials required.

> **Note:** This data feed is no longer available in the form the app expects. cdr.fyi now gates its full dataset; the public export has become a frozen snapshot (through Dec 31, 2023) with an added notice row and a changed column layout. As a result the data import no longer succeeds against the upstream sheet. The code is kept as-is to document how the original pipeline worked.

## Project structure

```
.
├── src/
│   ├── app.py                  # App entry point; builds the Dash app and exposes `server` for gunicorn
│   ├── assets/                 # CSS, logo, favicon (auto-served by Dash)
│   └── components/
│       ├── _00_own_ids.py      # Central registry of component IDs used across callbacks
│       ├── _01_import_cdr.py   # Loads and cleans the CDR data
│       ├── _02_layout.py       # Page layout, composing all components
│       ├── _03_date_select.py  # Date range picker + presets
│       ├── _03_method_dropdown.py
│       ├── _04_bar_plot.py     # Shared "top 10" bar chart builder
│       ├── _05_KPIs.py         # KPI indicator row
│       ├── _05_supplier_chart.py
│       ├── _05_purchaser_chart.py
│       ├── _06_price_chart.py
│       └── _07_pie_chart.py
├── EDA/                        # Exploratory notebooks behind the dashboard's metrics
├── render.yaml                 # Render deployment blueprint
└── requirements.txt
```

Each component exposes a `render(app, data)` function that returns a Dash layout fragment and registers its own callback — so the layout in `_02_layout.py` simply composes them. Numeric filename prefixes indicate render order in the layout.

## Running locally

Requires Python 3.10+.

```bash
# 1. Clone and enter the repo
git clone https://github.com/Finn-Feddersen/Stiesdal-CDR-Dashboard.git
cd Stiesdal-CDR-Dashboard

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
cd src
python app.py
```

Then open http://localhost:8051 in your browser.

## Deployment

The app deploys to [Render](https://render.com/) from `render.yaml` (a Render Blueprint). Render installs `requirements.txt` and starts the app with:

```bash
gunicorn --chdir src app:server
```

`app.py` exposes `server = app.server` for the WSGI server.

## Exploratory analysis (`EDA/`)

The `EDA/` folder holds the Jupyter notebooks used to prototype the metrics and chart logic before they were built into the dashboard:

- `supplier_tons_analysis.ipynb` — tons purchased and delivered, broken down by supplier
- `supplier_origin_analysis.ipynb` — tons delivered by supplier country/origin
- `cdr_method_contribution.ipynb` — share of volume by CDR method (purchased vs delivered)

These are kept for reference and are not part of the deployed app.
