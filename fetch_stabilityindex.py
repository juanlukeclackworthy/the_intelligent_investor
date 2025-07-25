from ib_insync import Stock
import xml.etree.ElementTree as ET
from collections import OrderedDict
from statistics import stdev

def compute_eps_stability_index(symbol, ib):
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

    # Sort and take last 6 years (to calculate 5 YoY changes)
    eps_by_date = OrderedDict(sorted(eps_by_date.items()))
    eps_values = list(eps_by_date.values())[-6:]

    if len(eps_values) < 6:
        print(f"{symbol}: ❌ Not enough EPS data.")
        return None

    yoy_growths = []
    for i in range(1, len(eps_values)):
        prev = eps_values[i - 1]
        curr = eps_values[i]
        if prev > 0:
            yoy_growths.append((curr - prev) / prev)

    if len(yoy_growths) < 2:
        print(f"{symbol}: ❌ Not enough YoY growth data.")
        return None

    vol = stdev(yoy_growths)
    stability = max(0, min(100, 100 - (vol * 200)))  # 0–100 index: higher = more stable

    return round(stability, 1)

