import inspect
import re
from io import BytesIO

from src.models import (
    CompanyProfile,
    FinancialMetrics,
    PriceStatistics,
    ResearchContext,
)
from src.services.report_service import ReportService


def make_context(*, missing_values: bool = False) -> ResearchContext:
    return ResearchContext(
        company=CompanyProfile(
            ticker="MSFT",
            name="Microsoft Corporation",
            sector=None if missing_values else "Technology",
            industry=None if missing_values else "Software - Infrastructure",
            market_cap=None if missing_values else 3_000_000_000_000,
        ),
        metrics=(
            FinancialMetrics(None, None, None, None, None)
            if missing_values
            else FinancialMetrics(
                revenue=245_000_000_000,
                net_income=88_000_000_000,
                pe_ratio=35.5,
                profit_margin=0.36,
                roe=0.33,
            )
        ),
        price_statistics=PriceStatistics(
            latest_close=105.0,
            period_high=110.0,
            period_low=90.0,
            average_volume=None if missing_values else 1_500_000,
        ),
        period="6mo",
    )


def test_markdown_contains_complete_context_and_analysis() -> None:
    report = ReportService().generate_markdown_report(
        make_context(), "Evidence-based AI analysis."
    )

    assert "Ticker: MSFT" in report
    assert "Name: Microsoft Corporation" in report
    assert "Sector: Technology" in report
    assert "Industry: Software - Infrastructure" in report
    assert "Market Cap: $3.00 T" in report
    assert "Revenue: $245.00 B" in report
    assert "Net Income: $88.00 B" in report
    assert "PE Ratio: 35.50" in report
    assert "Profit Margin: 36.00%" in report
    assert "ROE: 33.00%" in report
    assert "Period: 6mo" in report
    assert "Latest Close: $105" in report
    assert "Period High: $110" in report
    assert "Period Low: $90" in report
    assert "Average Volume: 1,500,000" in report
    assert "Evidence-based AI analysis." in report


def test_markdown_renders_missing_values_as_na() -> None:
    report = ReportService().generate_markdown_report(
        make_context(missing_values=True), "Summary"
    )

    assert report.count("N/A") == 9
    assert "None" not in report
    assert re.search(r"\b(?:nan|inf)\b", report, re.IGNORECASE) is None


def test_pdf_is_non_empty_readable_bytesio_from_same_context() -> None:
    context = make_context()

    pdf = ReportService().generate_pdf_report(context, "Deterministic summary")

    assert isinstance(pdf, BytesIO)
    assert pdf.tell() == 0
    assert pdf.read(4) == b"%PDF"
    assert len(pdf.getvalue()) > 1_000


def test_pdf_handles_missing_average_volume() -> None:
    pdf = ReportService().generate_pdf_report(
        make_context(missing_values=True), "Summary"
    )

    assert pdf.getvalue().startswith(b"%PDF")


def test_report_service_does_not_mutate_sys_path() -> None:
    import src.services.report_service as report_service_module

    source = inspect.getsource(report_service_module)
    assert "sys.path" not in source
