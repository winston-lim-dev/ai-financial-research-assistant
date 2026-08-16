from typing import Protocol

from src.models import ResearchContext
from src.services.ollama_generator import OllamaGenerator
from src.utils.helpers import (
    format_currency,
    format_market_cap,
    format_number,
    format_percentage,
)
from src.utils.logger import logger


class TextGenerator(Protocol):
    def generate(self, prompt: str) -> str: ...


class AnalysisService:
    def __init__(self, generator: TextGenerator | None = None) -> None:
        self._generator = generator or OllamaGenerator()

    def build_prompt(self, context: ResearchContext) -> str:
        company = context.company
        metrics = context.metrics
        prices = context.price_statistics

        return f"""You are preparing a concise, professional financial research summary.

Use only the supplied facts below. Distinguish observed facts from interpretation.
Do not invent or infer facts that are not supplied. Do not make claims about
competitive position, business moat, management quality, product quality, future
growth, unsupported risks, or investment attractiveness.
Do not provide investment advice or buy/sell recommendations. If a conclusion cannot be supported by the
available data, explicitly state that it cannot be determined. Treat N/A as
unavailable data, not as zero. Keep the response under 300 words.

Organize the response under these headings:
- Company Snapshot
- Profitability
- Valuation Snapshot
- Price Context
- Observed Strengths
- Observed Concerns
- Data Limitations

Supplied Research Context
-------------------------
Ticker: {company.ticker}
Company Name: {company.name}
Sector: {company.sector or 'N/A'}
Industry: {company.industry or 'N/A'}
Market Cap: {format_market_cap(company.market_cap)}

Revenue: {format_currency(metrics.revenue)}
Net Income: {format_currency(metrics.net_income)}
PE Ratio: {format_number(metrics.pe_ratio)}
Profit Margin: {format_percentage(metrics.profit_margin)}
Return on Equity (ROE): {format_percentage(metrics.roe)}

Selected Period: {context.period}
Latest Close: {format_currency(prices.latest_close)}
Period High: {format_currency(prices.period_high)}
Period Low: {format_currency(prices.period_low)}
Average Volume: {format_number(prices.average_volume, decimals=0)}
"""

    def generate_summary(self, context: ResearchContext) -> str:
        logger.info("Generating summary for %s", context.company.ticker)
        return self._generator.generate(self.build_prompt(context))
