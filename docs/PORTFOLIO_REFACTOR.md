# AI Financial Research Assistant — Portfolio Refactor

## Purpose

AI Financial Research Assistant is a local financial-research application built with Python, Streamlit, Yahoo Finance, Plotly, Ollama, and Llama 3.2.

The project already demonstrates:

* external financial-data integration;
* historical price analysis;
* basic financial metrics;
* interactive visualization;
* local LLM integration;
* AI-generated research summaries;
* Markdown and PDF report generation.

The purpose of this refactor is **not** to turn the application into a large financial platform.

The objective is to make it a compact, credible portfolio project demonstrating:

* clean external-data boundaries;
* typed financial models;
* deterministic financial analytics;
* constrained AI interpretation;
* automated testing;
* report generation;
* clear software-engineering decisions.

Bellcrank remains the higher-priority project and should receive substantially more long-term development effort.

This refactor must therefore remain deliberately bounded.

---

## Current Baseline

The current repository already has separate:

```text
app/
src/services/
src/utils/
tests/
docs/
```

Major existing services include:

```text
StockService
ChartService
AnalysisService
ReportService
```

The application currently retrieves:

* company profile data;
* historical prices;
* market capitalization;
* revenue;
* net income;
* trailing PE ratio;
* profit margin;
* return on equity.

It calculates:

* latest period close;
* period high;
* period low;
* average volume.

It then supplies financial data to a local Llama 3.2 model through Ollama and generates downloadable Markdown and PDF reports.

---

## Current Engineering Gaps

### Tests

The existing files under `tests/` are primarily manual smoke scripts rather than deterministic automated unit tests.

Some currently:

* call Yahoo Finance directly;
* call Ollama directly;
* execute code during module import;
* print results rather than assert behavior.

The refactor must replace these with proper automated tests.

### UI Coupling

`StockService` and `AnalysisService` currently depend directly on Streamlit caching.

Core application/service code should not depend on Streamlit.

Caching belongs at the application/composition boundary.

### Financial Data Modelling

Financial and company information are currently represented primarily as raw dictionaries.

The refactor should introduce a small number of explicit immutable models.

### Deterministic Analytics

Price statistics are currently calculated directly inside the Streamlit application.

Deterministic financial calculations should move into reusable, testable application code.

### AI Grounding

The current AI prompt requests qualitative conclusions such as business strengths, risks, and market position from a relatively small financial dataset.

The refactored prompt should distinguish:

* directly supplied facts;
* deterministic calculated metrics;
* constrained interpretation;
* unavailable information.

The AI should not be encouraged to infer unsupported business information.

### Report Consistency

Markdown and PDF reports should consume the same structured research context and expose consistent information.

---

## Portfolio Objective

The completed project should demonstrate the following pipeline:

```text
Yahoo Finance
      ↓
External Data Boundary
      ↓
Validated / Normalized Financial Models
      ↓
Deterministic Financial Analytics
      ↓
Research Context
      ↓
Constrained AI Interpretation
      ↓
Research Summary
      ↓
Streamlit + Markdown/PDF Reports
```

The project should be easy to:

1. understand;
2. run locally;
3. test without network or Ollama;
4. demonstrate;
5. explain during an interview or technical discussion.

The project does not need enterprise-scale architecture.

---

## Refactor Principles

### 1. Keep the architecture compact

Introduce only the abstractions needed to create meaningful boundaries.

Do not reproduce Bellcrank-level domain architecture.

### 2. Keep Streamlit thin

Streamlit should be responsible primarily for:

* user input;
* caching/composition;
* presentation;
* user-visible error handling.

It should not own:

* financial-data normalization;
* deterministic analytics;
* AI prompt construction;
* report business logic.

### 3. Isolate Yahoo Finance

Yahoo Finance should be accessed through one small external-data boundary.

Core services should not call `yfinance` directly throughout the application.

The boundary should be easy to replace with deterministic test data.

### 4. Use explicit financial models

Introduce small immutable models representing at least:

```text
CompanyProfile
FinancialMetrics
PriceStatistics
```

A combined research model such as:

```text
ResearchContext
```

may be introduced when justified.

Do not create a large financial-domain framework.

### 5. Keep deterministic facts separate from AI interpretation

The application should calculate financial facts deterministically where practical.

The LLM should interpret supplied facts rather than derive values that normal Python code can calculate reliably.

### 6. Constrain AI output

The AI prompt should:

* use only supplied information;
* avoid inventing financial facts;
* avoid unsupported claims about business quality or risk;
* identify data limitations;
* clearly distinguish factual observations from interpretation.

### 7. Test without external services

Normal `pytest` execution must not require:

* Yahoo Finance network access;
* Ollama;
* live market data;
* external APIs.

External boundaries should be replaceable with small deterministic fakes or stubs.

---

# Required Portfolio Scope

## Financial Data Boundary

Create a small Yahoo Finance adapter/provider responsible for obtaining raw external data.

Avoid repeated independent calls for the same company information where practical.

External failure behavior should be explicit.

Do not add another financial-data provider.

## Financial Models

Introduce immutable models for the financial information used by the application.

At minimum:

### CompanyProfile

Represent:

```text
ticker
name
sector
industry
market_cap
```

### FinancialMetrics

Represent:

```text
revenue
net_income
pe_ratio
profit_margin
roe
```

### PriceStatistics

Represent:

```text
latest_close
period_high
period_low
average_volume
```

Use optional values where external data may legitimately be missing.

Handle missing/non-finite values deliberately.

## Deterministic Analytics

Move price-statistic calculation out of Streamlit.

Calculation should handle:

* missing values;
* empty price history;
* non-finite numeric values where relevant.

Do not add large numbers of new financial ratios.

## Research Context

Create a coherent object representing the facts supplied to:

* AI analysis;
* Markdown reporting;
* PDF reporting.

Avoid passing long groups of loosely related dictionaries and scalar arguments through multiple services.

## AI Analysis

Remove Streamlit dependency from the AI service.

Keep Ollama as the production LLM integration.

Continue using:

```text
llama3.2:3b
```

unless an actual compatibility problem requires change.

The analysis prompt should focus on information actually supported by the supplied context.

A suitable structure may include:

```text
Company Snapshot
Profitability
Valuation Snapshot
Price Context
Observed Strengths
Observed Concerns
Data Limitations
```

The exact headings may differ.

Do not require sections that cannot be supported by the available data.

## Report Generation

Markdown and PDF generation should consume the same structured research context.

They should present consistent:

* company information;
* financial metrics;
* price statistics;
* AI analysis.

Avoid duplicated incompatible report logic where practical.

## Testing

Replace the existing smoke-script style tests with deterministic automated tests.

Tests should cover at least:

* financial-data normalization;
* missing Yahoo fields;
* invalid/unknown ticker behavior;
* deterministic price statistics;
* missing/non-finite price data;
* model construction;
* AI prompt construction;
* Ollama isolation;
* report generation;
* formatting behavior where important.

Normal tests must not contact Yahoo Finance or Ollama.

## Streamlit

Keep Streamlit as the user-facing application.

After the refactor it should mainly:

* collect ticker/period input;
* obtain/cache external data through the application boundary;
* invoke deterministic analysis;
* invoke AI analysis;
* render charts;
* render reports;
* display errors.

Do not redesign the entire UI.

---

# Explicitly Out of Scope

Do not implement during this portfolio refactor:

* Retrieval-Augmented Generation;
* vector databases;
* SEC filing ingestion;
* earnings-call transcription or analysis;
* news sentiment analysis;
* multi-company comparison;
* watchlists;
* live portfolio tracking;
* investment recommendation engines;
* valuation models requiring large new datasets;
* agents;
* LangGraph;
* FastAPI;
* PostgreSQL;
* Docker;
* cloud deployment;
* authentication;
* multiple financial-data providers;
* multiple LLM providers;
* complex production observability.

Document QA RAG already demonstrates RAG engineering.

Bellcrank already demonstrates deeper trading-system architecture and operational complexity.

This project should remain focused on:

**financial-data engineering + deterministic analytics + constrained AI interpretation.**

---

# Definition of Done

The portfolio refactor is complete when:

1. Yahoo Finance access is isolated behind a small external-data boundary.
2. Core financial information is represented by explicit immutable models.
3. Price statistics are calculated outside Streamlit.
4. Missing/non-finite financial values are handled deliberately.
5. A coherent research context is used across AI analysis and reports.
6. AI analysis no longer depends on Streamlit.
7. AI prompts avoid unsupported qualitative claims.
8. Markdown and PDF reports consume the same research context.
9. Automated tests run without Yahoo Finance network access or Ollama.
10. Streamlit is primarily a thin composition/presentation layer.
11. README accurately explains architecture, limitations, testing, and engineering decisions.
12. Screenshots accurately represent the final application.
13. No blocking portfolio-quality defects remain.

Once these conditions are satisfied, stop expanding the project.

Future development should be driven only by:

* an identified portfolio gap;
* employment-market evidence;
* a practical personal requirement.

---

# Implementation Sequence

## Step 1 — Financial Models and Data Boundary

* introduce immutable financial models;
* isolate Yahoo Finance;
* normalize external data;
* replace live stock-service smoke tests with deterministic tests;
* remove Streamlit dependency from core financial-data access.

## Step 2 — Research Context and Deterministic Analytics

* move price-statistic calculations out of Streamlit;
* create the structured research context;
* test deterministic calculations;
* update downstream consumers as needed.

## Step 3 — AI and Reporting Boundaries

* remove Streamlit dependency from AI analysis;
* constrain prompt behavior;
* isolate Ollama from tests;
* make Markdown and PDF reports consume the same research context;
* replace remaining smoke-script tests.

## Step 4 — Portfolio Finish

* simplify the Streamlit composition layer;
* remove prototype residue;
* review dependencies;
* verify application behavior;
* refresh screenshots;
* rewrite README;
* run complete tests;
* perform final definition-of-done review.

---

# Scope Rule

If a proposed change does not materially improve:

* financial-data engineering;
* deterministic analytics;
* AI grounding;
* testability;
* reliability;
* or portfolio presentation,

defer it.

Bellcrank remains the main long-term development priority.
