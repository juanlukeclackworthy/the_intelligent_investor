def apply_criteria(data):
    results = {}

    try:
        results['PE ≤ 17'] = float(data.get('PEEXCLXOR', 0)) <= 17
        results['3Y P/E ≤ 18'] = float(data.get('PE3YAVG', 0)) <= 18
        results['P/B ≤ 1.5'] = float(data.get('PB', 0)) <= 1.5
        results['Current Ratio > 2'] = float(data.get('CURRATIO', 0)) > 2
        results['Net Assets > Debt'] = float(data.get('QBVPS', 0)) > float(data.get('TOTDEBT', 1))
        results['Stability ≥ 75'] = float(data.get('STABILITY', 0)) >= 75
        results['EPS Growth ≥ 8%'] = True  # Placeholder: needs multi-year EPS
    except Exception as e:
        results['Error'] = str(e)

    return results
