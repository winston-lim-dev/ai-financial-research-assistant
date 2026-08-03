import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.services.stock_service import StockService

def test_company_lookup():

    service = StockService()

    result = service.get_price_history("MSFT","1d")

    assert result is not None

    return result


history = test_company_lookup()    
print(history.head())
print(history.columns)

service = StockService()

metrics = service.get_financial_metrics("MSFT")

print(metrics)
