from ib_insync import Stock
from datetime import datetime
from collections import OrderedDict
from statistics import mean
import xml.etree.ElementTree as ET

def compute_eps_absg_5y(symbol, ib):
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

    # Ensure EPS values are sorted by date: oldest → newest
    eps_by_date = OrderedDict(sorted(eps_by_date.items()))
    eps_values = list(eps_by_date.values())

    # Must have at least 5 years of EPS data
    if len(eps_values) < 5:
        print(f"{symbol}: Not enough valid EPS data.")
        return None, None

    # Get start (5 years ago) and end (most recent)
    start_eps = eps_values[-5]
    end_eps = eps_values[-1]

    try:
        growth = ((end_eps - start_eps) / abs(start_eps)) / 5
        return round(growth * 100, 2), list(eps_by_date.items())[-5:]
    except Exception as e:
        print(f"Absolute Growth calculation error for {symbol}: {e}")
        return None, list(eps_by_date.items())[-5:]
    

  

