from ib_insync import Stock
from utils import safe_cast
import xml.etree.ElementTree as ET

def extract_snapshot_fields(symbol, ib):
    contract = Stock(symbol, 'SMART', 'USD')
    snapshot = ib.reqFundamentalData(contract, reportType='ReportSnapshot')

    root = ET.fromstring(snapshot)
    data = {}

    for ratio in root.findall('.//Ratio'):
        field = ratio.get('FieldName')
        value = ratio.text
        if field and value:
            data[field] = value

    # Extract key ratios
    pe = safe_cast(data.get('PEEXCLXOR'))
    pb = safe_cast(data.get('PRICE2BK'))
  

    return pe, pb


