import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import streamlit as st
from src.services.stock_service import StockService
from src.utils.helpers import format_market_cap
from src.services.chart_service import ChartService

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
            template="plotly_white"
        )

        #fig.update_traces(
        #    line=dict(width=3)
        #)

        fig.update_traces(
            line=dict(
                color="green",
                width=4,
        )
)
        st.plotly_chart(
            fig,
            use_container_width=True
        )


    except ValueError as error:
        st.error(str(error))