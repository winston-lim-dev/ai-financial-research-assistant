# AI Financial Research Assistant

An AI-powered financial research platform built with Python, Streamlit, Yahoo Finance, Plotly, Ollama, and Llama 3.

The application retrieves company information, financial fundamentals, and historical stock price data, then generates AI-powered research summaries and downloadable research reports.

---

## Features

### Company Research

- Company Information Lookup
- Sector and Industry Identification
- Market Capitalization Analysis

### Financial Analysis

- Revenue
- Net Income
- PE Ratio
- Profit Margin
- Return on Equity (ROE)

### Historical Price Analysis

- 1 Month Price History
- 6 Month Price History
- 1 Year Price History
- Interactive Plotly Charts

### AI-Powered Research

- Local LLM Integration with Ollama
- Llama 3 Analysis
- Equity Research Style Summaries
- Business Strengths Assessment
- Risk Identification
- Market Position Analysis

### Report Generation

- Markdown Export
- PDF Export
- AI Research Summary Included

---

## Screenshots

### Dashboard

docs/screenshots/dashboard.png

### Historical Price Chart

docs/screenshots/chart.png

### AI Research Summary

docs/screenshots/ai analysis.png

### Export Report

docs/screenshots/report_download.png

---

## Tech Stack

### Backend

- Python
- yFinance
- Pandas

### Frontend

- Streamlit

### Data Visualization

- Plotly

### AI

- Ollama
- Llama 3

### Report Generation

- ReportLab

### Testing

- Pytest

### Development Tools

- Git
- GitHub
- VS Code

---

## Architecture

Streamlit UI
     │
     ▼
Service Layer
     │
     ├── StockService
     ├── ChartService
     ├── AnalysisService
     └── ReportService
     │
     ▼
External Services
     │
     ├── Yahoo Finance
     └── Ollama (Llama 3)
```

---

## Project Structure

```text
ai-financial-research-assistant/

├── app/
│   ├── __init__.py
│   └── streamlit_app.py
│
├── data/
│
├── docs/
│   ├── architecture.md
│   └── screenshots/
│
├── src/
│   ├── __init__.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── stock_service.py
│   │   ├── chart_service.py
│   │   ├── analysis_service.py
│   │   └── report_service.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── cache.py
│       ├── helpers.py
│       └── logger.py
│
├── tests/
│   ├── test_stock_service.py
│   ├── test_analysis_service.py
│   └── test_report_service.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

---

## How It Works

### 1. User Searches a Ticker

Example:

```text
MSFT
```

### 2. Financial Data Retrieval

The application retrieves:

- Company Information
- Financial Metrics
- Historical Price Data

using Yahoo Finance.

### 3. Visualization

Historical stock prices are displayed through interactive Plotly charts.

### 4. AI Analysis

Financial metrics and market data are passed to Llama 3 through Ollama.

The AI generates:

- Company Overview
- Financial Health Assessment
- Valuation Commentary
- Business Strengths
- Potential Risks

### 5. Report Export

Users can export:

- Markdown Research Reports
- PDF Research Reports

---

## Installation

### Clone Repository

```bash
git clone https://github.com/winston-lim-dev/ai-financial-research-assistant.git

cd ai-financial-research-assistant

python -m venv .venv

pip install -r requirements.txt

streamlit run app/streamlit_app.py

```

### Create Virtual Environment

#### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

#### macOS/Linux

```bash
python -m venv .venv

source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Ollama Setup

Install Ollama:

```bash
https://ollama.com
```

Pull the Llama3.2:3b model:

```bash
ollama pull llama3
```

Verify installation:

```bash
ollama list
```

---

## Running the Application

Start Ollama:

```bash
ollama serve
```

Run Streamlit:

```bash
streamlit run app/streamlit_app.py
```

The application will open automatically in your browser.

---

## Running Tests

Run all tests:

```bash
pytest
```

Run a specific test file:

```bash
pytest tests/test_stock_service.py
```

---

## Git Workflow

This project follows a feature branch workflow.

```text
main
│
develop
│
├── feature/project-setup
├── feature/stock-data-service
├── feature-price-history
├── feature-ai-analysis
└── feature-report-export
```

---

## Future Enhancements

### Version 1.1

- Multi-Company Comparison
- Watchlist Functionality
- Additional Financial Ratios

### Version 1.2

- Earnings Call Analysis
- SEC Filing Analysis
- News Sentiment Analysis

### Version 2.0

- Financial RAG System
- Vector Database Integration
- Earnings Report Question Answering
- Multi-Document Research Assistant

---

## Learning Objectives

This project was built to develop practical experience with:

- API Integration
- Financial Data Analysis
- Data Visualization
- Local LLM Deployment
- AI Application Development
- Report Automation
- Software Architecture
- Git Feature Branch Workflow
- Testing and Documentation

---

## License

MIT License

---

## Author

Winston Lim

Portfolio Project #2

AI Financial Research Assistant