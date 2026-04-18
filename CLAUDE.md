# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r projeto-acoes/requirements.txt

# Run the app (Flask dev server on http://localhost:5000)
python projeto-acoes/app.py
```

No test framework is configured.

## Architecture

Single-page Flask web app that displays a Brazilian stock market (B3) dashboard with interactive Plotly charts.

**`projeto-acoes/data.py`** — Data layer. `get_stock_data()` fetches 2025 historical data for PETR4, ITUB4, and VALE3 via yfinance, computes cumulative return percentages, and returns a combined pandas DataFrame.

**`projeto-acoes/app.py`** — Application layer. `build_charts(df)` converts the DataFrame into 3 Plotly figures (historical close price, cumulative returns, daily volume). The single Flask route `/` calls both functions and passes chart JSON to the template.

**`projeto-acoes/templates/index.html`** — Presentation layer. Jinja2 template receives serialized Plotly chart data and renders them via Plotly.js (CDN). Dark theme (`#111827`/`#1f2937` backgrounds). UI text is in Portuguese (pt-BR).

**Data flow**: request → `get_stock_data()` → `build_charts()` → `render_template()` → browser renders Plotly charts.
