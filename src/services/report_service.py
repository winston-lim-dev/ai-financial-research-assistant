import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from datetime import datetime
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet

from src.utils.helpers import format_currency
from src.utils.helpers import format_percentage
from src.utils.helpers import format_market_cap

class ReportService:

    def generate_markdown_report(
        self,
        company: dict,
        metrics: dict,
        summary: str,
        current_price: float,
        period_high: float,
        period_low: float,
        average_volume: float | int | None,
    ) -> str:
        return f"""
# Financial Research Report

Generated:
{datetime.now().strftime("%Y-%m-%d")}

## Company Information

Name: {company['name']}

Sector: {company['sector']}

Industry: {company['industry']}

Market Cap: {format_market_cap(company['market_cap'])}

## Financial Metrics

Revenue: {format_currency(metrics['revenue'])}

Net Income: {format_currency(metrics['net_income'])}

PE Ratio: {metrics['pe_ratio']}

Profit Margin: {format_percentage(metrics['profit_margin'])}

ROE: {format_percentage(metrics['roe'])}

## AI Research Summary

{summary}
"""

    def generate_pdf_report(
        self,
        company: dict,
        metrics: dict,
        summary: str,
        current_price: float,
        period_high: float,
        period_low: float,
        average_volume: float | int | None,
    ) -> BytesIO:

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph("Financial Research Report", styles["Title"])
        )

        average_volume_text = (
            f"{average_volume:,.0f}" if average_volume is not None else "N/A"
        )

        elements.append(
            Paragraph(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                styles["Normal"],
            )
        )

        elements.append(Spacer(1, 12))

        elements.append(
            Paragraph("Company Information", styles["Heading2"])
        )

        elements.append(
            Paragraph(
                f"""
                Name: {company.get("name", "N/A")}<br/>
                Sector: {company.get("sector", "N/A")}<br/>
                Industry: {company.get("industry", "N/A")}<br/>
                Market Cap: {format_market_cap(company.get("market_cap", "N/A"))}
                """,
                styles["Normal"],
            )
        )

        elements.append(Spacer(1, 12))

        elements.append(
            Paragraph("Financial Metrics", styles["Heading2"])
        )

        elements.append(
            Paragraph(
                f"""
                Revenue: {format_currency(metrics.get("revenue", "N/A"))}<br/>
                Net Income: {format_currency(metrics.get("net_income", "N/A"))}<br/>
                PE Ratio: {metrics.get("pe_ratio", "N/A")}<br/>
                Profit Margin: {format_percentage(metrics.get("profit_margin", "N/A"))}<br/>
                ROE: {format_percentage(metrics.get("roe", "N/A"))}
                """,
                styles["Normal"],
            )
        )

        elements.append(Spacer(1, 12))

        elements.append(
            Paragraph("Price Statistics", styles["Heading2"])
        )

        elements.append(
            Paragraph(
                f"""
                Current Price: ${current_price:.2f}<br/>
                Period High: ${period_high:.2f}<br/>
                Period Low: ${period_low:.2f}<br/>
                Average Volume: {average_volume_text}
                """,
                styles["Normal"],
            )
        )

        elements.append(Spacer(1, 12))

        elements.append(
            Paragraph("AI Research Summary", styles["Heading2"])
        )

        elements.append(
            Paragraph(summary.replace("\n", "<br/>"), styles["Normal"])
        )

        doc.build(elements)

        buffer.seek(0)

        return buffer
