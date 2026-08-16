from datetime import datetime
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from src.models import ResearchContext
from src.utils.helpers import (
    format_currency,
    format_market_cap,
    format_number,
    format_percentage,
)


def _text(value: str | None) -> str:
    return value if value else "N/A"


class ReportService:
    def generate_markdown_report(
        self, context: ResearchContext, summary: str
    ) -> str:
        company = context.company
        metrics = context.metrics
        prices = context.price_statistics

        return f"""# Financial Research Report

Generated: {datetime.now().strftime('%Y-%m-%d')}

## Company Information

Ticker: {company.ticker}

Name: {company.name}

Sector: {_text(company.sector)}

Industry: {_text(company.industry)}

Market Cap: {format_market_cap(company.market_cap)}

## Financial Metrics

Revenue: {format_currency(metrics.revenue)}

Net Income: {format_currency(metrics.net_income)}

PE Ratio: {format_number(metrics.pe_ratio)}

Profit Margin: {format_percentage(metrics.profit_margin)}

ROE: {format_percentage(metrics.roe)}

## Price Statistics

Period: {context.period}

Latest Close: {format_currency(prices.latest_close)}

Period High: {format_currency(prices.period_high)}

Period Low: {format_currency(prices.period_low)}

Average Volume: {format_number(prices.average_volume, decimals=0)}

## AI Research Summary

{summary}
"""

    def generate_pdf_report(
        self, context: ResearchContext, summary: str
    ) -> BytesIO:
        company = context.company
        metrics = context.metrics
        prices = context.price_statistics
        styles = getSampleStyleSheet()
        buffer = BytesIO()
        elements = [
            Paragraph("Financial Research Report", styles["Title"]),
            Paragraph(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                styles["Normal"],
            ),
            Spacer(1, 12),
            Paragraph("Company Information", styles["Heading2"]),
            Paragraph(
                self._pdf_lines(
                    ("Ticker", company.ticker),
                    ("Name", company.name),
                    ("Sector", _text(company.sector)),
                    ("Industry", _text(company.industry)),
                    ("Market Cap", format_market_cap(company.market_cap)),
                ),
                styles["Normal"],
            ),
            Spacer(1, 12),
            Paragraph("Financial Metrics", styles["Heading2"]),
            Paragraph(
                self._pdf_lines(
                    ("Revenue", format_currency(metrics.revenue)),
                    ("Net Income", format_currency(metrics.net_income)),
                    ("PE Ratio", format_number(metrics.pe_ratio)),
                    ("Profit Margin", format_percentage(metrics.profit_margin)),
                    ("ROE", format_percentage(metrics.roe)),
                ),
                styles["Normal"],
            ),
            Spacer(1, 12),
            Paragraph("Price Statistics", styles["Heading2"]),
            Paragraph(
                self._pdf_lines(
                    ("Period", context.period),
                    ("Latest Close", format_currency(prices.latest_close)),
                    ("Period High", format_currency(prices.period_high)),
                    ("Period Low", format_currency(prices.period_low)),
                    (
                        "Average Volume",
                        format_number(prices.average_volume, decimals=0),
                    ),
                ),
                styles["Normal"],
            ),
            Spacer(1, 12),
            Paragraph("AI Research Summary", styles["Heading2"]),
            Paragraph(escape(summary).replace("\n", "<br/>"), styles["Normal"]),
        ]

        SimpleDocTemplate(buffer).build(elements)
        buffer.seek(0)
        return buffer

    @staticmethod
    def _pdf_lines(*items: tuple[str, object]) -> str:
        return "<br/>".join(
            f"{escape(label)}: {escape(str(value))}" for label, value in items
        )
