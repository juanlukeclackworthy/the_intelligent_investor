import pandas as pd
from ib_connect import connect_ib
from fetch_5yravgpe import compute_5yr_avg_pe

# Get tickers
url = "https://datahub.io/core/s-and-p-500-companies/r/constituents.csv"
df = pd.read_csv(url)
tickers = df['Symbol'].tolist()[:10]
# Connect to IBKR ONCE
ib = connect_ib(client_id=1001)  # use a unique client ID

# ['MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADBE', 'AMD', 'AES', 'AFL', 'A']

# Loop through tickers
for ticker in tickers:
    try:
        avg_pe, pe_list = compute_5yr_avg_pe(ticker, ib, verbose=False)

        if avg_pe is not None:
            if any(pe < 0 for pe in pe_list):
                print(f"⚠️ Negative PE alert: {ticker}")
            if avg_pe < 15:
                print(f"\n✅ {ticker}: {avg_pe:.2f} (5-year average P/E < 15)")
                print("Last 5 Yearly P/E values:")
                for i, pe in enumerate(pe_list, 1):
                    sign = "🔴" if pe < 0 else "🟢"
                    print(f"  {i}. {sign} P/E = {pe:.2f}")
                print("-" * 40)

    except Exception as e:
        print(f"{ticker}: ❌ Failed with error: {e}")
 
            








