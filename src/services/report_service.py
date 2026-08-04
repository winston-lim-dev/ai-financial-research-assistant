from datetime import datetime


class ReportService:

    def generate_markdown_report(
        self,
        company,
        metrics,
        summary,
    ):

        return f"""
# Financial Research Report

Generated:
{datetime.now().strftime("%Y-%m-%d")}

## Company Information

Name: {company['name']}

Sector: {company['sector']}

Industry: {company['industry']}

Market Cap: {company['market_cap']}

## Financial Metrics

Revenue: {metrics['revenue']}

Net Income: {metrics['net_income']}

PE Ratio: {metrics['pe_ratio']}

Profit Margin: {metrics['profit_margin']}

ROE: {metrics['roe']}

## AI Research Summary

{summary}
"""