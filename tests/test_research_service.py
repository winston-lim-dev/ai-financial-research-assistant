from dataclasses import FrozenInstanceError

import pandas as pd
import pytest

from src.models import (
    CompanyProfile,
    FinancialMetrics,
    PriceStatistics,
    ResearchContext,
)
from src.services.research_service import (
    ResearchService,
    calculate_price_statistics,
)


COMPANY = CompanyProfile(
    ticker="MSFT",
    name="Microsoft Corporation",
    sector="Technology",
    industry="Software - Infrastructure",
    market_cap=3_000_000_000_000,
)
METRICS = FinancialMetrics(
    revenue=245_000_000_000,
    net_income=88_000_000_000,
    pe_ratio=35.5,
    profit_margin=0.36,
    roe=0.33,
)


class FakeStockService:
    def __init__(self, history: pd.DataFrame) -> None:
        self.history = history
        self.company_requests: list[str] = []
        self.history_requests: list[tuple[str, str]] = []

    def get_company_data(
        self, ticker: str
    ) -> tuple[CompanyProfile, FinancialMetrics]:
        self.company_requests.append(ticker)
        return COMPANY, METRICS

    def get_price_history(self, ticker: str, period: str) -> pd.DataFrame:
        self.history_requests.append((ticker, period))
        return self.history


def test_calculates_valid_price_statistics() -> None:
    history = pd.DataFrame(
        {"Close": [101.0, 99.0, 105.0], "Volume": [100, 200, 300]}
    )

    statistics = calculate_price_statistics(history)

    assert statistics == PriceStatistics(
        latest_close=105.0,
        period_high=105.0,
        period_low=99.0,
        average_volume=200.0,
    )


def test_ignores_nan_and_infinite_close_values() -> None:
    history = pd.DataFrame(
        {
            "Close": [float("nan"), 98.0, float("inf"), float("-inf"), 102.0],
            "Volume": [1, 2, 3, 4, 5],
        }
    )

    statistics = calculate_price_statistics(history)

    assert statistics.latest_close == 102.0
    assert statistics.period_high == 102.0
    assert statistics.period_low == 98.0


def test_ignores_nan_and_infinite_volume_values() -> None:
    history = pd.DataFrame(
        {
            "Close": [100.0, 101.0, 102.0],
            "Volume": [50.0, float("nan"), float("inf")],
        }
    )

    assert calculate_price_statistics(history).average_volume == 50.0


@pytest.mark.parametrize(
    "history",
    [
        pd.DataFrame(),
        pd.DataFrame({"Close": [float("nan"), float("inf"), float("-inf")]}),
    ],
)
def test_rejects_history_without_usable_closing_prices(
    history: pd.DataFrame,
) -> None:
    with pytest.raises(ValueError, match="empty|no usable closing prices"):
        calculate_price_statistics(history)


def test_rejects_missing_history() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        calculate_price_statistics(None)


@pytest.mark.parametrize(
    "history",
    [
        pd.DataFrame({"Close": [100.0]}),
        pd.DataFrame(
            {
                "Close": [100.0, 101.0],
                "Volume": [float("nan"), float("-inf")],
            }
        ),
    ],
)
def test_no_usable_volume_produces_none(history: pd.DataFrame) -> None:
    assert calculate_price_statistics(history).average_volume is None


def test_price_statistics_is_immutable() -> None:
    statistics = PriceStatistics(100.0, 101.0, 99.0, None)

    with pytest.raises(FrozenInstanceError):
        statistics.latest_close = 1.0  # type: ignore[misc]


def test_build_context_preserves_models_statistics_period_and_history() -> None:
    history = pd.DataFrame({"Close": [100.0, 103.0], "Volume": [10, 30]})
    stock_service = FakeStockService(history)

    result = ResearchService(stock_service).build_context("msft", "6mo")

    assert result.context.company is COMPANY
    assert result.context.metrics is METRICS
    assert result.context.price_statistics == PriceStatistics(
        latest_close=103.0,
        period_high=103.0,
        period_low=100.0,
        average_volume=20.0,
    )
    assert result.context.period == "6mo"
    assert result.history is history
    assert stock_service.company_requests == ["msft"]
    assert stock_service.history_requests == [("msft", "6mo")]


def test_research_context_is_immutable() -> None:
    context = ResearchContext(
        company=COMPANY,
        metrics=METRICS,
        price_statistics=PriceStatistics(100.0, 101.0, 99.0, None),
        period="1y",
    )

    with pytest.raises(FrozenInstanceError):
        context.period = "1mo"  # type: ignore[misc]


def test_research_service_has_no_streamlit_dependency() -> None:
    import src.services.research_service as research_service_module

    assert "streamlit" not in research_service_module.__dict__
