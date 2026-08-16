from dataclasses import dataclass
from typing import Any, Protocol

from src.models import (
    CompanyProfile,
    FinancialMetrics,
    PriceStatistics,
    ResearchContext,
)
from src.utils.numbers import normalize_finite_number


@dataclass(frozen=True)
class ResearchResult:
    """Application result carrying domain facts plus chart transport data."""

    context: ResearchContext
    history: Any


class ResearchStockService(Protocol):
    def get_company_data(
        self, ticker: str
    ) -> tuple[CompanyProfile, FinancialMetrics]: ...

    def get_price_history(self, ticker: str, period: str = "1y") -> Any: ...


def calculate_price_statistics(history: Any) -> PriceStatistics:
    if history is None or history.empty:
        raise ValueError("Price history must not be empty")
    if "Close" not in history.columns:
        raise ValueError("Price history does not contain closing prices")

    closes = [
        number
        for value in history["Close"]
        if (number := normalize_finite_number(value)) is not None
    ]
    if not closes:
        raise ValueError("Price history contains no usable closing prices")

    volumes = []
    if "Volume" in history.columns:
        volumes = [
            number
            for value in history["Volume"]
            if (number := normalize_finite_number(value)) is not None
        ]

    return PriceStatistics(
        latest_close=closes[-1],
        period_high=max(closes),
        period_low=min(closes),
        average_volume=sum(volumes) / len(volumes) if volumes else None,
    )


class ResearchService:
    def __init__(self, stock_service: ResearchStockService) -> None:
        self._stock_service = stock_service

    def build_context(self, ticker: str, period: str) -> ResearchResult:
        company, metrics = self._stock_service.get_company_data(ticker)
        history = self._stock_service.get_price_history(ticker, period)
        context = ResearchContext(
            company=company,
            metrics=metrics,
            price_statistics=calculate_price_statistics(history),
            period=period,
        )
        return ResearchResult(context=context, history=history)
