from yahooquery import Ticker

def get_current_ratio(symbol):
    ticker = Ticker(symbol)
    bs = ticker.balance_sheet(frequency='annual')

    try:
        latest = bs[bs['asOfDate'] == bs['asOfDate'].max()]
        ca = latest['CurrentAssets'].values[0]
        cl = latest['CurrentLiabilities'].values[0]

        current_ratio = ca / cl
        return round(current_ratio, 2)  # <-- Return the value

    except Exception as e:
        return None  # Return None or another sentinel value on error
    
print(get_current_ratio('AAPL'))

