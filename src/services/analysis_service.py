import ollama
from src.utils.logger import logger

class AnalysisService:

    def _build_prompt(
        self,
        company: dict,
        current_price: float,
        period_high: float,
        period_low: float,
    ) -> str:

        return f"""
You are a financial research analyst.

Provide:

1. Company Overview
2. Business Strengths
3. Potential Risks
4. Market Position

Use clear business language.
Limit response to 250 words.

Company: {company['name']}
Sector: {company['sector']}
Industry: {company['industry']}
Market Cap: {company['market_cap']}

Current Price: ${current_price:.2f}
Period High: ${period_high:.2f}
Period Low: ${period_low:.2f}
"""

    def generate_summary(
        self,
        company: dict,
        current_price: float,
        period_high: float,
        period_low: float,
    ) -> str:

        logger.info(f"Generating summary")

        prompt = self._build_prompt(
            company,
            current_price,
            period_high,
            period_low,
        )

        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]

