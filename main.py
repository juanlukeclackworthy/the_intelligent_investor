import pandas as pd
from ib_connect import connect_ib
from fetch_5yravgpe import compute_5yr_avg_pe
from fetch_5yabsg import compute_eps_absg_5y
from fetch_currentratio import get_current_ratio
from fetch_ibkr_snapshot import extract_snapshot_fields
from fetch_stabilityindex import compute_eps_stability_index

# Get tickers
url = "https://datahub.io/core/s-and-p-500-companies/r/constituents.csv"
df = pd.read_csv(url)
tickers = df['Symbol'].tolist()[100:]

# Connect to IBKR ONCE
ib = connect_ib(client_id=1001)

for ticker in tickers:
    try:
        # P/E calculation
        avg_pe, pe_list, pe_details = compute_5yr_avg_pe(ticker, ib, verbose=False)
    except Exception as e:
        print(f"{ticker}: ❌ compute_5yr_avg_pe failed: {e}")
        continue

    try:
        # Other metrics
        fiveabsgrowth, last_5_eps = compute_eps_absg_5y(ticker, ib)
        currentratio = get_current_ratio(ticker)
        snap_pe, snap_pb = extract_snapshot_fields(ticker, ib)
        stability = compute_eps_stability_index(ticker, ib)

        # Check filter conditions
        base_conditions_met = (
            avg_pe is not None and avg_pe < 15 and
            fiveabsgrowth is not None and last_5_eps is not None and fiveabsgrowth >= 6 and
            snap_pb is not None and snap_pb <= 2.5 and
            snap_pe is not None and snap_pe < 17
        )

        if not base_conditions_met:
            continue

        # Warn on negative EPS
        for date, eps in last_5_eps:
            if eps <= 0:
                print(f"{ticker}: Negative EPS in last 5 years — Year: {date}, EPS: {eps}")

        # Print pass results
        if currentratio is not None and currentratio > 1.5:
            print(f"\n✅ {ticker}")
            print(f"Snapshot P/E:  {snap_pe:.2f}")
            print(f"Snapshot P/B:  {snap_pb:.2f}")
            print(f"Current Ratio: {currentratio:.2f}")
            print(f"5yr_avg_pe:    {avg_pe:.2f}")
            print(f"EPS ABS Growth:{fiveabsgrowth:.2f}%")
            print(f"Stability:     {stability}")

        elif currentratio is None:
            print(f"\n📘 {ticker} (likely financial)")
            print(f"Snapshot P/E:  {snap_pe:.2f}")
            print(f"Snapshot P/B:  {snap_pb:.2f}")
            print(f"Current Ratio: N/A")
            print(f"5yr_avg_pe:    {avg_pe:.2f}")
            print(f"EPS ABS Growth:{fiveabsgrowth:.2f}%")
            print(f"Stability:     {stability}")
        else:
            continue  # Current ratio filter failed

        # Detailed breakdown
        print("\nDetailed Yearly Breakdown:")
        printed_dates = set()
        for date, eps, close, pe in pe_details:
            if pe in pe_list and date not in printed_dates:
                print(f"{date} | EPS: {eps:.2f} | Close: {close:.2f} | P/E: {pe:.2f}")
                printed_dates.add(date)

        print("-" * 60)

    except Exception as e:
        print(f"{ticker}: ❌ Failed with error: {e}")
