import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import streamlit as st

from src.services.analysis_service import AnalysisService
from src.services.chart_service import ChartService
from src.services.report_service import ReportService
from src.services.research_service import ResearchService
from src.services.stock_service import StockService
from src.utils.helpers import (
    format_currency,
    format_market_cap,
    format_number,
    format_percentage,
)


stock_service = StockService()
research_service = ResearchService(stock_service)
chart_service = ChartService()
analysis_service = AnalysisService()
report_service = ReportService()


@st.cache_data(ttl=3600)
def generate_summary_cached(context):
    return analysis_service.generate_summary(context)


st.title("AI Financial Research Assistant")

ticker = st.text_input("Enter Stock Ticker", placeholder="MSFT")

with st.sidebar:
    st.subheader("Application Settings")
    if st.button("Refresh AI Cache"):
        st.cache_data.clear()
        st.session_state.pop("summary", None)
        st.success("AI cache cleared")
        st.rerun()

if not ticker:
    st.stop()

period_options = {
    "1 Month": "1mo",
    "6 Months": "6mo",
    "1 Year": "1y",
}
selected_period = st.selectbox("Time Period", list(period_options))
period = period_options[selected_period]

research_key = (ticker.strip().upper(), period)
if st.session_state.get("last_research_key") != research_key:
    st.session_state.pop("summary", None)
    st.session_state.last_research_key = research_key

try:
    research_result = research_service.build_context(ticker, period)
except ValueError as error:
    st.error(str(error))
    st.stop()
except Exception as error:
    st.error("Unable to retrieve financial data from Yahoo Finance.")
    st.exception(error)
    st.stop()

context = research_result.context
company = context.company
metrics = context.metrics
prices = context.price_statistics

st.subheader(company.name)
st.write(f"Ticker: {company.ticker}")
st.write(f"Sector: {company.sector or 'N/A'}")
st.write(f"Industry: {company.industry or 'N/A'}")
st.write(f"Market Cap: {format_market_cap(company.market_cap)}")

price_columns = st.columns(4)
price_columns[0].metric("Latest Close", f"${prices.latest_close:.2f}")
price_columns[1].metric("Period High", f"${prices.period_high:.2f}")
price_columns[2].metric("Period Low", f"${prices.period_low:.2f}")
price_columns[3].metric(
    "Avg Volume", format_number(prices.average_volume, decimals=0)
)

figure = chart_service.create_price_chart(research_result.history)
figure.update_layout(
    title="Price History",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    template="plotly_white",
    margin=dict(l=20, r=20, t=50, b=20),
)
figure.update_traces(
    mode="lines+markers",
    marker=dict(size=4),
    line=dict(color="green", width=4),
    hovertemplate=(
        "<b>Date</b>: %{x}<br>"
        "<b>Price</b>: $%{y:.2f}<extra></extra>"
    ),
)
st.plotly_chart(figure, width="stretch")

st.subheader("Financial Metrics")
metric_columns = st.columns(3)
metric_columns[0].metric("Revenue", format_currency(metrics.revenue))
metric_columns[1].metric("Net Income", format_currency(metrics.net_income))
metric_columns[2].metric("PE Ratio", format_number(metrics.pe_ratio))

ratio_columns = st.columns(2)
ratio_columns[0].metric(
    "Profit Margin", format_percentage(metrics.profit_margin)
)
ratio_columns[1].metric("ROE", format_percentage(metrics.roe))

if st.button("Generate AI Analysis"):
    try:
        with st.spinner("Generating AI Analysis..."):
            st.session_state.summary = generate_summary_cached(context)
    except Exception as error:
        st.error(
            "AI analysis is unavailable. Confirm Ollama is running and "
            "llama3.2:3b is installed."
        )
        st.exception(error)

if "summary" in st.session_state:
    summary = st.session_state.summary
    st.subheader("AI Research Summary")
    st.markdown(summary)

    try:
        markdown_report = report_service.generate_markdown_report(context, summary)
        pdf_report = report_service.generate_pdf_report(context, summary)
    except Exception as error:
        st.error("Unable to generate downloadable reports.")
        st.exception(error)
    else:
        download_columns = st.columns(2)
        with download_columns[0]:
            st.download_button(
                label="Download Markdown Report",
                data=markdown_report,
                file_name=f"{company.ticker}_research_report.md",
                mime="text/markdown",
            )
        with download_columns[1]:
            st.download_button(
                label="Download PDF Report",
                data=pdf_report,
                file_name=f"{company.ticker}_research_report.pdf",
                mime="application/pdf",
            )
