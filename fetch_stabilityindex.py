from ib_insync import Stock
import xml.etree.ElementTree as ET
from ib_connect import connect_ib
from collections import defaultdict
from collections import OrderedDict
from datetime import datetime
from statistics import mean,stdev
from statistics import stdev

def compute_eps_stability_index(symbol):
    ib = connect_ib()
    stock = Stock(symbol, 'SMART', 'USD')
    summary = ib.reqFundamentalData(stock, 'ReportsFinSummary')
    root = ET.fromstring(summary)

    eps_by_date = OrderedDict()
    for eps in root.findall(".//EPS"):
        attrs = eps.attrib
        if attrs.get("reportType") == "A" and attrs.get("period") == "12M":
            asof_date = attrs.get("asofDate")
            try:
                eps_by_date[asof_date] = float(eps.text)
            except:
                continue

    eps_values = list(eps_by_date.values())[:5]
    if len(eps_values) < 5:
        print("❌ Not enough EPS data.")
        return None

    yoy_growths = []
    for i in range(1, 5):
        prev = eps_values[i]
        curr = eps_values[i - 1]
        if prev > 0:
            yoy_growths.append((curr - prev) / prev)

    if len(yoy_growths) < 2:
        print("❌ Not enough YoY growth data.")
        return None

    vol = stdev(yoy_growths)
    stability = max(0, min(100, 100 - (vol * 200)))
    print(f"EPS Volatility for {symbol}: {vol*100:.2f}%")
    print(f"Stability Index for {symbol}: {stability:.1f}")
    return round(stability, 1)

compute_eps_stability_index('AAPL')
