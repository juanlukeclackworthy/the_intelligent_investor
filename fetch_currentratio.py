from yahooquery import Ticker
import pandas as pd

def get_current_ratio(symbol):
    ticker = Ticker(symbol)
    bs = ticker.balance_sheet(frequency='annual')

    try:
        # If bs is a dict (common), extract symbol's data
        if isinstance(bs, dict):
            bs = bs.get(symbol, pd.DataFrame())

        if bs.empty:
            print(f"❌ No balance sheet data for {symbol}")
            return None

        latest = bs[bs['asOfDate'] == bs['asOfDate'].max()]

        if 'CurrentAssets' not in latest.columns or 'CurrentLiabilities' not in latest.columns:
            return None

        ca = latest['CurrentAssets'].values[0]
        cl = latest['CurrentLiabilities'].values[0]

        return round(ca / cl, 2)

    except Exception as e:
        print(f"❌ Error for {symbol}: {e}")
        return None


