import yfinance as yf
import streamlit as st

from src.utils.logger import logger

@st.cache_data(ttl=3600)
def get_price_history_cached(ticker: str, period: str):
    stock = yf.Ticker(ticker.upper())
    return stock.history(period=period)

@st.cache_data(ttl=3600)
def get_company_info_cached(ticker: str):
    stock = yf.Ticker(ticker.upper())
    return stock.info

@st.cache_data(ttl=3600)
def get_financial_metrics_cached(ticker: str):
    stock = yf.Ticker(ticker.upper())
    return stock.info

class StockService:
    def get_company_info(self, ticker: str) -> dict:

        try:

            logger.info(f"Fetching ticker: {ticker}")

            info = get_company_info_cached(ticker)

            if "longName" not in info:
                logger.warning(f"Invalid ticker: {ticker}")
                
                raise ValueError(
                    f"Invalid ticker: {ticker}"
                )

            result = {
                "ticker": ticker.upper(),
                "name": info.get("longName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "market_cap": info.get("marketCap"),
            }

            logger.info(f"Successfully retrieved data for {ticker}")

            return result

        except Exception as e:
            logger.error(f"Error retrieving {ticker}: {e}")
            raise

    def get_price_history(self,ticker: str,period: str = "1y"):

        logger.info(f"Fetching history: {ticker}")

        history = get_price_history_cached(ticker, period)

        if history.empty:

            logger.info(f"No history found for {ticker}")

            raise ValueError(
                f"No historical data found for {ticker}"
            )

        logger.info(f"Successfully retrieved history for {ticker}")

        return history

    def get_financial_metrics(self, ticker: str) -> dict:

        logger.info(f"Fetching financial metrics: {ticker}")

        info = get_financial_metrics_cached(ticker)

        return {
            "revenue": info.get("totalRevenue"),
            "net_income": info.get("netIncomeToCommon"),
            "pe_ratio": info.get("trailingPE"),
            "profit_margin": info.get("profitMargins"),
            "roe": info.get("returnOnEquity"),
        }
