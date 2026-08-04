
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.services.report_service import ReportService
from src.services.stock_service import StockService
from src.services.analysis_service import AnalysisService

report_service = ReportService()
stock_service = StockService()
analysis_service = AnalysisService()

company = {
    "name": "Microsoft Corporation",
    "sector": "Technology",
    "industry": "Software",
    "market_cap": 3800000000000
}

metrics = stock_service.get_financial_metrics("msft")

history = stock_service.get_price_history(
    "msft",
    "1y"
)

close = history["Close"].dropna()
latest_price = close.iloc[-1]
highest_price = close.max()
lowest_price = close.min()

volume = history["Volume"].dropna()
avg_volume = volume.mean()

summary = analysis_service.generate_summary(
    company, 
    metrics,
    latest_price,
    highest_price,
    lowest_price
)

report = report_service.generate_markdown_report(
    company,
    metrics,
    summary, 

)

print(report)