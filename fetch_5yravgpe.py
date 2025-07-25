from ib_insync import Stock
from datetime import datetime
from collections import OrderedDict
from statistics import mean
import xml.etree.ElementTree as ET

def compute_5yr_avg_pe(symbol, ib, verbose=True):
    if verbose:
        print(f"\n{symbol}")  # Print ticker name

    stock = Stock(symbol, 'SMART', 'USD')
    summary = ib.reqFundamentalData(stock, 'ReportsFinSummary')
    root = ET.fromstring(summary)

    # Parse EPS data
    eps_by_date = OrderedDict()
    for eps in root.findall(".//EPS"):
        attrs = eps.attrib
        if attrs.get("reportType") == "A" and attrs.get("period") == "12M":
            asof_date = attrs.get("asofDate")
            try:
                eps_by_date[asof_date] = float(eps.text)
            except:
                continue

    # Compute P/E ratios
    pe_by_date = {}
    pe_details = []  # Store (date, eps, close, pe) for display

    for asof_date, eps_value in eps_by_date.items():
        bars = ib.reqHistoricalData(
            stock,
            endDateTime=datetime.strptime(asof_date, "%Y-%m-%d").strftime("%Y%m%d %H:%M:%S"),
            durationStr='1 D',
            barSizeSetting='1 day',
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1
        )
        if bars:
            close_price = bars[-1].close
            try:
                pe_ratio = close_price / eps_value
                pe_by_date[asof_date] = pe_ratio
                pe_details.append((asof_date, eps_value, close_price, pe_ratio))
            except ZeroDivisionError:
                continue

    # Sort by date descending
    sorted_pe = sorted(pe_by_date.items(), reverse=True)
    last_5_keys = [date for date, _ in sorted_pe[:5]]
    last_5_pe = [pe_by_date[date] for date in last_5_keys]

    if len(last_5_pe) < 5:
        if verbose:
            print("❌ Not enough data for 5-year average.")
        return None, last_5_pe, pe_details

    avg = mean(last_5_pe)
    
    if verbose:
        print(f"5-year P/E Average: {avg:.2f}")
        for entry in pe_details:
            asof_date, eps, close, pe = entry
            if asof_date in last_5_keys:
                print(f"{asof_date} | EPS: {eps:.2f} | Close: {close:.2f} | P/E: {pe:.2f}")

    return round(avg, 2), last_5_pe, pe_details


