from ib_insync import Stock
from datetime import datetime
from collections import OrderedDict
from statistics import mean
import xml.etree.ElementTree as ET
from ib_connect import connect_ib

def compute_eps_cagr_5y(symbol):
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
    if len(eps_values) < 5 or eps_values[4] <= 0:
        print("❌ Not enough valid EPS data.")
        return None

    cagr = (eps_values[0] / eps_values[4]) ** (1/5) - 1
    print(f"5y EPS CAGR for {symbol}: {cagr:.2%}")
    return round(cagr * 100, 2)

compute_eps_cagr_5y('AAPL')
