
# Fundamental Stock Screener – IBKR API

This project is a Python-based stock screener that connects to Interactive Brokers (IBKR) using the `ib_insync` API. It extracts and evaluates fundamental financial data for listed equities based on custom investment criteria.

The tool supports value-focused and quality-oriented investment strategies by computing key financial ratios and analyzing 5-year historical trends.

---

## Key Takeaways & Limitations

This project highlighted several important insights and areas for improvement in stock screening workflows:

1. **Need for Broader Time Series**  
   - Limiting analysis to 5 years reduces visibility into long-term business cycles. A 10+ year horizon is often needed for meaningful quality signals.

2. **Custom Database Required for Scale**  
   - Pulling large datasets from APIs like IBKR can be slow. Storing normalized data locally enables faster queries and multi-factor filtering.

3. **EPS Data Needs Standardization**  
   - Variations between reported and adjusted EPS (e.g., GAAP vs. non-GAAP) lead to inconsistent calculations. A structured approach to distinguish and standardize earnings is essential.

4. **Lack of Public Benchmarking Tools**  
   - Most free screening tools are limited in flexibility and historical depth. There is a clear gap in robust, transparent platforms for backtesting value metrics.

5. **Filter Complexity Requires Deeper Research**  
   - Simple filters (like P/E or P/B) are useful, but miss important context such as debt levels, capital intensity, reinvestment rates, and earnings quality. Integrating more complex filters is key to improving selectivity.

---

## Features

The screener collects and calculates the following metrics:

- **Snapshot P/E (PEEXCLXOR)** – Price-to-Earnings ratio from the latest IBKR snapshot  
- **Snapshot P/B (PRICE2BK)** – Price-to-Book ratio from IBKR  
- **Current Ratio** – Measures short-term liquidity (where available)  
- **5-Year Average P/E** – Derived from historical EPS and price data  
- **5-Year EPS Absolute Growth** – Compound annual growth rate (CAGR) of EPS  
- **Stability Index** – Measures consistency of earnings over 5 years

---

## Technology Stack

- **Language**: Python 3.8+
- **Libraries**:  
  - `ib_insync` – Interactive Brokers API access  
  - `xml.etree.ElementTree` – XML parsing  
  - `pandas` – Data handling  
- **IBKR Gateway or TWS**: Required for API connectivity

---

## Sample Screening Results

### PHM (Consumer Discretionary)

| Metric                  | Value    |
|-------------------------|----------|
| Snapshot P/E            | 7.68     |
| Snapshot P/B            | 1.78     |
| Current Ratio           | 11.08    |
| 5-Year Average P/E      | 7.26     |
| EPS Absolute Growth     | 37.11%   |
| Stability Index         | 65.6     |

**5-Year Historical Breakdown:**

| Year | EPS   | Close Price | P/E   |
|------|-------|-------------|-------|
| 2024 | 14.82 | 108.86      | 7.35  |
| 2023 | 11.79 | 103.22      | 8.75  |
| 2022 | 11.07 | 45.53       | 4.11  |
| 2021 | 7.44  | 56.65       | 7.61  |
| 2020 | 5.19  | 44.09       | 8.50  |

---

### Summary – Financial Sector Examples

| Ticker | Snapshot P/E | P/B   | 5yr Avg P/E | EPS Growth | Stability |
|--------|---------------|-------|--------------|-------------|-----------|
| RF     | 11.90         | 1.32  | 10.99        | 17.67%      | 0.0       |
| STT    | 12.26         | 1.36  | 12.05        | 6.03%       | 48.8      |
| SYF    | 9.51          | 1.72  | 8.29         | 55.79%      | 0.0       |
| TRV    | 13.96         | 2.06  | 13.08        | 21.21%      | 32.9      |

**Note**: Current ratio is not typically reported for financial institutions.

---

## Errors and Missing Data

The following tickers could not be processed due to data unavailability or formatting issues:

- **No fundamentals available**: SW, SOLV, SMCI, TEL, TKO  
- **No historical price data**: TPL

---

## How to Run

1. Ensure Interactive Brokers TWS or Gateway is running with API access enabled.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the main script:
   ```bash
   python main.py
   ```

---

## Future Enhancements

- Expand analysis to 10–15 years of history  
- Build a local SQLite or PostgreSQL database with update scripts  
- Add filters for:
  - Net Asset Value vs. Debt
  - Debt/Equity ratio
  - Return on Invested Capital (ROIC)
  - Free Cash Flow Yield  
- Export data to dashboards, CSVs, or web UI  
- Introduce benchmarking vs. ETFs or factor indices
