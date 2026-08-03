import yfinance as yf
from src.utils.logger import logger

class StockService:
    def get_company_info(self, ticker: str) -> dict:

        try:

            logger.info(f"Fetching ticker: {ticker}")

            stock = yf.Ticker(ticker.upper())

            info = stock.info

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

        stock = yf.Ticker(ticker.upper())

        history = stock.history(period=period)

        if history.empty:

            logger.info(f"No history found for {ticker}")

            raise ValueError(
                f"No historical data found for {ticker}"
            )

        logger.info(f"Successfully retrieved history for {ticker}")

        return history
