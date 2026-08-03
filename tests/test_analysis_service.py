import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.services.analysis_service import AnalysisService

service = AnalysisService()

company = {
    "name": "Microsoft Corporation",
    "sector": "Technology",
    "industry": "Software",
    "market_cap": "3.8T",
}

summary = service.generate_summary(
    company,
    current_price=520.15,
    period_high=540.10,
    period_low=410.25,
)

print(summary)