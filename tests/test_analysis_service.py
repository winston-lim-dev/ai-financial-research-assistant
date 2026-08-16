from typing import Any

from src.models import (
    CompanyProfile,
    FinancialMetrics,
    PriceStatistics,
    ResearchContext,
)
from src.services.analysis_service import AnalysisService
from src.services.ollama_generator import OllamaGenerator


def make_context(*, missing_metrics: bool = False) -> ResearchContext:
    return ResearchContext(
        company=CompanyProfile(
            ticker="MSFT",
            name="Microsoft Corporation",
            sector="Technology",
            industry="Software - Infrastructure",
            market_cap=3_000_000_000_000,
        ),
        metrics=(
            FinancialMetrics(None, None, None, None, None)
            if missing_metrics
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
            average_volume=1_500_000,
        ),
        period="6mo",
    )


class FakeGenerator:
    def __init__(self, output: str = "Deterministic analysis") -> None:
        self.output = output
        self.prompts: list[str] = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.output


def test_analysis_accepts_context_passes_prompt_and_returns_output() -> None:
    generator = FakeGenerator("Exact generator output")

    result = AnalysisService(generator).generate_summary(make_context())

    assert result == "Exact generator output"
    assert len(generator.prompts) == 1


def test_prompt_contains_company_metrics_prices_and_period() -> None:
    prompt = AnalysisService(FakeGenerator()).build_prompt(make_context())

    assert "MSFT" in prompt
    assert "Microsoft Corporation" in prompt
    assert "Technology" in prompt
    assert "Revenue: $245.00 B" in prompt
    assert "Net Income: $88.00 B" in prompt
    assert "PE Ratio: 35.50" in prompt
    assert "Profit Margin: 36.00%" in prompt
    assert "Latest Close: $105" in prompt
    assert "Period High: $110" in prompt
    assert "Period Low: $90" in prompt
    assert "Average Volume: 1,500,000" in prompt
    assert "Selected Period: 6mo" in prompt


def test_prompt_represents_missing_metrics_as_unavailable() -> None:
    prompt = AnalysisService(FakeGenerator()).build_prompt(
        make_context(missing_metrics=True)
    )

    assert "Revenue: N/A" in prompt
    assert "Net Income: N/A" in prompt
    assert "PE Ratio: N/A" in prompt
    assert "Profit Margin: N/A" in prompt
    assert "Return on Equity (ROE): N/A" in prompt
    assert "None" not in prompt


def test_prompt_constrains_invention_advice_and_data_limitations() -> None:
    prompt = AnalysisService(FakeGenerator()).build_prompt(make_context())

    assert "Do not invent or infer facts" in prompt
    assert "Do not provide investment advice or buy/sell recommendations" in prompt
    assert "cannot be supported" in prompt
    assert "Data Limitations" in prompt
    assert "Observed Strengths" in prompt
    assert "Observed Concerns" in prompt


def test_ollama_generator_uses_default_model_without_live_service(
    monkeypatch,
) -> None:
    calls: list[dict[str, Any]] = []

    def fake_chat(**kwargs: Any) -> dict[str, dict[str, str]]:
        calls.append(kwargs)
        return {"message": {"content": "Local fake response"}}

    monkeypatch.setattr("src.services.ollama_generator.ollama.chat", fake_chat)

    generator = OllamaGenerator()
    result = generator.generate("Test prompt")

    assert generator.model == "llama3.2:3b"
    assert result == "Local fake response"
    assert calls == [
        {
            "model": "llama3.2:3b",
            "messages": [{"role": "user", "content": "Test prompt"}],
        }
    ]


def test_analysis_service_has_no_streamlit_dependency() -> None:
    import src.services.analysis_service as analysis_service_module

    assert "streamlit" not in analysis_service_module.__dict__
