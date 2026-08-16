from collections.abc import Mapping
from dataclasses import FrozenInstanceError

import pandas as pd
import pytest

from src.models import CompanyProfile, FinancialMetrics
from src.services.stock_service import StockService


VALID_INFO = {
    "longName": "Microsoft Corporation",
    "sector": "Technology",
    "industry": "Software - Infrastructure",
    "marketCap": 3_000_000_000_000,
    "totalRevenue": 245_000_000_000,
    "netIncomeToCommon": 88_000_000_000,
    "trailingPE": 35.5,
    "profitMargins": 0.36,
    "returnOnEquity": 0.33,
}


class FakeProvider:
    def __init__(
        self,
        info: Mapping[str, object] | None = None,
        history: pd.DataFrame | None = None,
    ) -> None:
        self.info = VALID_INFO if info is None else info
        self.history = (
            pd.DataFrame({"Close": [100.0], "Volume": [1_000]})
            if history is None
            else history
        )
        self.info_tickers: list[str] = []
        self.history_requests: list[tuple[str, str]] = []

    def get_info(self, ticker: str) -> Mapping[str, object]:
        self.info_tickers.append(ticker)
        return self.info

    def get_history(self, ticker: str, period: str) -> pd.DataFrame:
        self.history_requests.append((ticker, period))
        return self.history


def test_company_data_normalizes_ticker_and_maps_both_models_once() -> None:
    provider = FakeProvider()

    company, metrics = StockService(provider).get_company_data("  msft ")

    assert company == CompanyProfile(
        ticker="MSFT",
        name="Microsoft Corporation",
        sector="Technology",
        industry="Software - Infrastructure",
        market_cap=3_000_000_000_000,
    )
    assert metrics == FinancialMetrics(
        revenue=245_000_000_000,
        net_income=88_000_000_000,
        pe_ratio=35.5,
        profit_margin=0.36,
        roe=0.33,
    )
    assert provider.info_tickers == ["MSFT"]


@pytest.mark.parametrize("ticker", ["", " ", "\t\n"])
def test_empty_ticker_is_rejected_without_calling_provider(ticker: str) -> None:
    provider = FakeProvider()

    with pytest.raises(ValueError, match="Ticker must not be empty"):
        StockService(provider).get_company_info(ticker)

    assert provider.info_tickers == []


def test_missing_optional_fields_become_none() -> None:
    provider = FakeProvider({"longName": "Known Company"})

    company, metrics = StockService(provider).get_company_data("known")

    assert company == CompanyProfile("KNOWN", "Known Company", None, None, None)
    assert metrics == FinancialMetrics(None, None, None, None, None)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_financial_values_become_none(value: float) -> None:
    info = dict(VALID_INFO)
    for field in (
        "marketCap",
        "totalRevenue",
        "netIncomeToCommon",
        "trailingPE",
        "profitMargins",
        "returnOnEquity",
    ):
        info[field] = value

    company, metrics = StockService(FakeProvider(info)).get_company_data("msft")

    assert company.market_cap is None
    assert metrics == FinancialMetrics(None, None, None, None, None)


@pytest.mark.parametrize(
    "info", [{}, {"longName": None}, {"longName": "   "}, {"symbol": "NOPE"}]
)
def test_unknown_ticker_without_usable_company_identity_is_rejected(
    info: Mapping[str, object],
) -> None:
    with pytest.raises(ValueError, match="Invalid ticker: NOPE"):
        StockService(FakeProvider(info)).get_company_info(" nope ")


def test_history_uses_provider_boundary_with_normalized_ticker() -> None:
    provider = FakeProvider()

    history = StockService(provider).get_price_history(" msft ", "6mo")

    assert not history.empty
    assert provider.history_requests == [("MSFT", "6mo")]


def test_empty_history_is_rejected() -> None:
    provider = FakeProvider(history=pd.DataFrame())

    with pytest.raises(ValueError, match="No historical data found for MSFT"):
        StockService(provider).get_price_history("msft")


def test_financial_models_are_immutable() -> None:
    company = CompanyProfile("MSFT", "Microsoft", None, None, None)

    with pytest.raises(FrozenInstanceError):
        company.name = "Changed"  # type: ignore[misc]


def test_stock_service_has_no_streamlit_dependency() -> None:
    import src.services.stock_service as stock_service_module

    assert "streamlit" not in stock_service_module.__dict__
