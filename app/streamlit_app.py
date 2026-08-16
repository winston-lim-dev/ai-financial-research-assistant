import sys
from dataclasses import asdict
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import streamlit as st

from src.services.stock_service import StockService
from src.services.chart_service import ChartService
from src.services.analysis_service import AnalysisService
from src.services.report_service import ReportService
from src.services.research_service import ResearchService

from src.utils.helpers import format_market_cap
from src.utils.helpers import format_currency
from src.utils.helpers import format_percentage

service = StockService()
research_service = ResearchService(service)
chart_service = ChartService()
analysis_service = AnalysisService()
report_service = ReportService()

st.title("AI Financial Research Assistant")

ticker = st.text_input(
    "Enter Stock Ticker",
    placeholder="MSFT"
)

if "last_ticker" not in st.session_state:
    st.session_state.last_ticker = ""

if ticker != st.session_state.last_ticker:
    st.session_state.pop("summary", None)
    st.session_state.last_ticker = ticker

with st.sidebar:

    st.subheader("Application Settings")

    if st.button("Refresh AI Cache"):
        st.cache_data.clear()
        st.success("AI cache cleared")
        st.rerun()

if ticker:

    try:
        period_options = {
            "1 Month": "1mo",
            "6 Months": "6mo",
            "1 Year": "1y"
        }

        selected_period = st.selectbox(
            "Time Period",
            list(period_options.keys())
        )

        period = period_options[selected_period]

        research_result = research_service.build_context(ticker, period)
        context = research_result.context
        company = context.company
        metrics = context.metrics
        price_statistics = context.price_statistics
        history = research_result.history

        st.subheader(company.name)

        st.write(f"Sector: {company.sector}")
        st.write(f"Industry: {company.industry}")
        st.write(f"Market Cap: {format_market_cap(company.market_cap)}")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Latest Close",
            f"${price_statistics.latest_close:.2f}"
        )

        col2.metric(
            "Period High",
            f"${price_statistics.period_high:.2f}"
        )

        col3.metric(
            "Period Low",
            f"${price_statistics.period_low:.2f}"
        )

        col4.metric(
            "Avg Volume",
            (
                f"{price_statistics.average_volume:,.0f}"
                if price_statistics.average_volume is not None
                else "N/A"
            )
        )

        fig = chart_service.create_price_chart(
            history
        )

        fig.update_layout(
            title="Price History",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white",
            margin=dict(l=20, r=20, t=50, b=20)
        )

        #fig.update_traces(
        #    line=dict(width=3)
        #)

        fig.update_traces(
            mode="lines+markers",
            marker=dict(size=4),
            line=dict(
                color="green",
                width=4,
            ),
            hovertemplate=
                "<b>Date</b>: %{x}<br>"
                "<b>Price</b>: $%{y:.2f}<extra></extra>"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

                # Display metrics
        st.subheader("Financial Metrics")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Revenue",
            format_currency(metrics.revenue)
        )

        col2.metric(
            "Net Income",
            format_currency(metrics.net_income)
        )

        col3.metric(
            "PE Ratio",
            metrics.pe_ratio
        )

        col4, col5 = st.columns(2)

        col4.metric(
            "Profit Margin",
            format_percentage(
                metrics.profit_margin
            )
        )

        col5.metric(
            "ROE",
            format_percentage(
                metrics.roe
            )
        )


        if st.button("Generate AI Analysis"):

            with st.spinner("Generating AI Analysis..."):

                st.session_state.summary = analysis_service.generate_summary(
                    company=asdict(company),
                    metrics=asdict(metrics),
                    current_price=price_statistics.latest_close,
                    period_high=price_statistics.period_high,
                    period_low=price_statistics.period_low,
                )

        if "summary" in st.session_state:

            st.subheader("AI Research Summary")
            st.markdown(st.session_state.summary)

            markdown_report = report_service.generate_markdown_report(
                company=asdict(company),
                metrics=asdict(metrics),
                summary=st.session_state.summary,
                current_price=price_statistics.latest_close,
                period_high=price_statistics.period_high,
                period_low=price_statistics.period_low,
                average_volume=price_statistics.average_volume,
            )

            pdf_report = report_service.generate_pdf_report(
                company=asdict(company),
                metrics=asdict(metrics),
                summary=st.session_state.summary,
                current_price=price_statistics.latest_close,
                period_high=price_statistics.period_high,
                period_low=price_statistics.period_low,
                average_volume=price_statistics.average_volume,
            )

            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    label="Download Markdown Report",
                    data=markdown_report,
                    file_name=f"{ticker}_research_report.md",
                    mime="text/markdown",
                )

            with col2:
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_report,
                    file_name=f"{ticker}_research_report.pdf",
                    mime="application/pdf",
    )            

    except ValueError as error:
        st.error(str(error))
