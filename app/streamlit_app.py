import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import streamlit as st
from src.services.stock_service import StockService
from src.utils.helpers import format_market_cap

service = StockService()

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

    except ValueError as error:
        st.error(str(error))