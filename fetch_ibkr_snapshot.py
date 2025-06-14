from ib_connect import connect_ib
from utils import safe_cast
from ib_insync import Stock
import xml.etree.ElementTree as ET

def extract_snapshot_fields(symbol):
    ib = connect_ib(client_id=101)
    contract = Stock(symbol, 'SMART', 'USD')
    snapshot = ib.reqFundamentalData(contract, reportType='ReportSnapshot')

    root = ET.fromstring(snapshot)
    data = {}
    
    for ratio in root.findall('.//Ratio'):
        field = ratio.get('FieldName')
        value = ratio.text
        if field and value:
            data[field] = value
    
    pe = safe_cast(data.get('PEEXCLXOR'))
    pb = safe_cast(data.get('PRICE2BK'))

    print(f"P/E: {pe}")
    print(f"P/B: {pb}")
    return pe, pb  # ✅ only if you added this

print(extract_snapshot_fields('AAPL'))
