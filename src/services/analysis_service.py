import ollama
from src.utils.logger import logger

class AnalysisService:

    def _build_prompt(
        self,
        company: dict,
        metrics: dict,
        current_price: float,
        period_high: float,
        period_low: float,
    ) -> str:

        return f"""
You are a professional equity research analyst.

Analyze the company using the provided data and produce:

1. Company Overview
2. Financial Health
3. Valuation Considerations
4. Business Strengths
5. Potential Risks

Guidelines:
- Use only the provided information.
- Do not invent financial data.
- Keep the response under 300 words.
- Write in a professional research style.

Company Information
-------------------
Company Name: {company.get('name')}
Sector: {company.get('sector')}
Industry: {company.get('industry')}
Market Cap: {company.get('market_cap')}

Financial Metrics
-----------------
Revenue: {metrics.get('revenue')}
Net Income: {metrics.get('net_income')}
PE Ratio: {metrics.get('pe_ratio')}
Profit Margin: {metrics.get('profit_margin')}
Return on Equity (ROE): {metrics.get('roe')}

Price Information
-----------------
Current Price: ${current_price:.2f}
Period High: ${period_high:.2f}
Period Low: ${period_low:.2f}
"""

    def generate_summary(
        self,
        company: dict,
        metrics: dict,
        current_price: float,
        period_high: float,
        period_low: float,
    ) -> str:

        logger.info(f"Generating summary")


        prompt = self._build_prompt(
            company=company,
            metrics=metrics,
            current_price=current_price,
            period_high=period_high,
            period_low=period_low,
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