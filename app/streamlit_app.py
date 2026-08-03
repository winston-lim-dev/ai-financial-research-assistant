import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import streamlit as st

from src.services.stock_service import StockService
from src.services.chart_service import ChartService
from src.services.analysis_service import AnalysisService 

from src.utils.helpers import format_market_cap
from src.utils.helpers import format_currency
from src.utils.helpers import format_percentage

service = StockService()
chart_service = ChartService()

st.title("AI Financial Research Assistant")

ticker = st.text_input(
    "Enter Stock Ticker",
    placeholder="MSFT"
)

if ticker:

    try:
        company = service.get_company_info(ticker)

        st.subheader(company["name"])

        st.write(f"Sector: {company['sector']}")
        st.write(f"Industry: {company['industry']}")
        st.write(f"Market Cap: {format_market_cap(company['market_cap'])}")

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


        history = service.get_price_history(
            ticker,
            period
        )

        latest_price = history["Close"].iloc[-1]
        highest_price = history["Close"].max()
        lowest_price = history["Close"].min()
        avg_volume = history["Volume"].mean()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Current Price",
            f"${latest_price:.2f}"
        )

        col2.metric(
            "Period High",
            f"${highest_price:.2f}"
        )

        col3.metric(
            "Period Low",
            f"${lowest_price:.2f}"
        )

        col4.metric(
            "Avg Volume",
            f"{avg_volume:,.0f}"
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
        metrics = service.get_financial_metrics(ticker)

        st.subheader("Financial Metrics")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Revenue",
            format_currency(metrics["revenue"])
        )

        col2.metric(
            "Net Income",
            format_currency(metrics["net_income"])
        )

        col3.metric(
            "PE Ratio",
            metrics["pe_ratio"]
        )

        col4, col5 = st.columns(2)

        col4.metric(
            "Profit Margin",
            format_percentage(
                metrics["profit_margin"]
            )
        )

        col5.metric(
            "ROE",
            format_percentage(
                metrics["roe"]
            )
        )
 
        summary = AnalysisService.generate_summary(
            company=company,
            metrics=metrics,
            current_price=latest_price,
            period_high=highest_price,
            period_low=lowest_price,
        )

        st.subheader("AI Analysis")
        st.write(summary)

    except ValueError as error:
        st.error(str(error))