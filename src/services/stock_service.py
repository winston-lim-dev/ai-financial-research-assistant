import yfinance as yf


class StockService:
    def get_company_info(self, ticker: str) -> dict:

        stock = yf.Ticker(ticker.upper())

        info = stock.info

        if "longName" not in info:
            raise ValueError(
                f"Invalid ticker: {ticker}"
            )

        return {
            "ticker": ticker.upper(),
            "name": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "market_cap": info.get("marketCap"),
        }