from collections.abc import Mapping
from typing import Any

import yfinance as yf


class YahooFinanceProvider:
    """Small boundary around the yfinance API used by the application."""

    def get_info(self, ticker: str) -> Mapping[str, object]:
        return yf.Ticker(ticker).info

    def get_history(self, ticker: str, period: str) -> Any:
        return yf.Ticker(ticker).history(period=period)
