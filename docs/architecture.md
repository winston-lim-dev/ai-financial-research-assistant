# Architecture

The application uses a small service pipeline with external integrations kept at
the edges.

```text
Streamlit composition layer
    |
    +--> ResearchService
    |        |-- StockService
    |        |       `-- YahooFinanceProvider --> yfinance
    |        `-- deterministic price-statistic calculation
    |
    +--> ResearchContext
             |-- CompanyProfile
             |-- FinancialMetrics
             `-- PriceStatistics
                    |-- AnalysisService --> OllamaGenerator --> Ollama
                    `-- ReportService --> Markdown / PDF
```

## Boundaries

- **YahooFinanceProvider** is the only module that constructs `yfinance.Ticker`
  objects. It returns raw external information and history.
- **StockService** normalizes tickers and external financial values, validates a
  usable company identity and history, and creates `CompanyProfile` and
  `FinancialMetrics`.
- **ResearchService** obtains company data and history once per research flow,
  calculates deterministic price statistics, and builds `ResearchContext`. Raw
  history is returned separately for charting rather than stored in the domain
  model.
- **ResearchContext** is the immutable collection of facts shared downstream.
- **AnalysisService** builds the grounded prompt from `ResearchContext` and delegates
  text generation to an injected generator.
- **OllamaGenerator** is the production LLM boundary and uses `llama3.2:3b`.
- **ReportService** creates consistent Markdown and PDF representations from the
  same `ResearchContext` and AI summary.
- **Streamlit** composes services, caches AI output, manages interaction and session
  state, renders charts and metrics, exposes downloads, and reports user-facing
  errors.

Core financial, analytics, AI, and report services do not depend on Streamlit.
