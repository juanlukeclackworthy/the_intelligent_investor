from yahooquery import Ticker

def net_assets_exceed_debt(symbol):
    ticker = Ticker(symbol)
    bs = ticker.balance_sheet(frequency='annual')

    try:
        latest = bs[bs['asOfDate'] == bs['asOfDate'].max()]
        equity = latest['StockholdersEquity'].values[0]
        debt = latest['TotalDebt'].values[0]

        net_assets_gt_debt = equity > debt

        if net_assets_gt_debt:
            print("✅ Net Assets > Debt")
        else:
            print("❌ Net Assets ≤ Debt")

        return net_assets_gt_debt

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

print(net_assets_exceed_debt('AAPL'))