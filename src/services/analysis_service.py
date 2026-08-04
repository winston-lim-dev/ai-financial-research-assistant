import ollama
import streamlit as st

from src.utils.logger import logger

from src.utils.helpers import format_percentage
from src.utils.helpers import format_market_cap
from src.utils.helpers import format_currency

@st.cache_data(ttl=3600)
def generate_summary_cached(
    model: str,
    prompt: str
):

    return ollama.chat(
        model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

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
6. Market Position

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
Market Cap: {format_market_cap(company.get('market_cap'))}

Financial Metrics
-----------------
Revenue: {format_currency(metrics.get('revenue'))}
Net Income: {format_currency(metrics.get('net_income'))}
PE Ratio: {metrics.get('pe_ratio')}
Profit Margin: {format_percentage(metrics.get('profit_margin'))}
Return on Equity (ROE): {format_percentage(metrics.get('roe'))}

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

        response = generate_summary_cached("llama3.2:3b",prompt)

        return response["message"]["content"]