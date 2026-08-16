from collections.abc import Mapping
from typing import Any, Protocol

from src.models import CompanyProfile, FinancialMetrics
from src.services.yahoo_finance_provider import YahooFinanceProvider
from src.utils.logger import logger
from src.utils.numbers import normalize_finite_number


class FinancialDataProvider(Protocol):
    def get_info(self, ticker: str) -> Mapping[str, object]: ...

    def get_history(self, ticker: str, period: str) -> Any: ...


def _normalize_ticker(ticker: str) -> str:
    normalized = ticker.strip().upper()
    if not normalized:
        raise ValueError("Ticker must not be empty")
    return normalized


class StockService:
    def __init__(self, provider: FinancialDataProvider | None = None) -> None:
        self._provider = provider or YahooFinanceProvider()

    def get_company_data(
        self, ticker: str
    ) -> tuple[CompanyProfile, FinancialMetrics]:
        """Fetch one info payload and map it to both public financial models."""
        normalized_ticker = _normalize_ticker(ticker)
        logger.info("Fetching company data: %s", normalized_ticker)
        info = self._provider.get_info(normalized_ticker)
        return (
            self._company_profile_from_info(normalized_ticker, info),
            self._financial_metrics_from_info(info),
        )

    def get_company_info(self, ticker: str) -> CompanyProfile:
        normalized_ticker = _normalize_ticker(ticker)
        logger.info("Fetching ticker: %s", normalized_ticker)
        info = self._provider.get_info(normalized_ticker)
        return self._company_profile_from_info(normalized_ticker, info)

    def get_financial_metrics(self, ticker: str) -> FinancialMetrics:
        normalized_ticker = _normalize_ticker(ticker)
        logger.info("Fetching financial metrics: %s", normalized_ticker)
        info = self._provider.get_info(normalized_ticker)
        return self._financial_metrics_from_info(info)

    def get_price_history(self, ticker: str, period: str = "1y") -> Any:
        normalized_ticker = _normalize_ticker(ticker)
        logger.info("Fetching history: %s", normalized_ticker)
        history = self._provider.get_history(normalized_ticker, period)
        if history.empty:
            raise ValueError(
                f"No historical data found for {normalized_ticker}"
            )
        return history

    @staticmethod
    def _company_profile_from_info(
        ticker: str, info: Mapping[str, object]
    ) -> CompanyProfile:
        name = info.get("longName")
        if not isinstance(name, str) or not name.strip():
            logger.warning("Invalid ticker: %s", ticker)
            raise ValueError(f"Invalid ticker: {ticker}")

        sector = info.get("sector")
        industry = info.get("industry")
        return CompanyProfile(
            ticker=ticker,
            name=name.strip(),
            sector=sector if isinstance(sector, str) else None,
            industry=industry if isinstance(industry, str) else None,
            market_cap=normalize_finite_number(info.get("marketCap")),
        )

    @staticmethod
    def _financial_metrics_from_info(
        info: Mapping[str, object]
    ) -> FinancialMetrics:
        return FinancialMetrics(
            revenue=normalize_finite_number(info.get("totalRevenue")),
            net_income=normalize_finite_number(info.get("netIncomeToCommon")),
            pe_ratio=normalize_finite_number(info.get("trailingPE")),
            profit_margin=normalize_finite_number(info.get("profitMargins")),
            roe=normalize_finite_number(info.get("returnOnEquity")),
        )
