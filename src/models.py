from dataclasses import dataclass


FinancialNumber = int | float


@dataclass(frozen=True)
class CompanyProfile:
    ticker: str
    name: str
    sector: str | None
    industry: str | None
    market_cap: FinancialNumber | None


@dataclass(frozen=True)
class FinancialMetrics:
    revenue: FinancialNumber | None
    net_income: FinancialNumber | None
    pe_ratio: FinancialNumber | None
    profit_margin: FinancialNumber | None
    roe: FinancialNumber | None


@dataclass(frozen=True)
class PriceStatistics:
    latest_close: FinancialNumber
    period_high: FinancialNumber
    period_low: FinancialNumber
    average_volume: FinancialNumber | None


@dataclass(frozen=True)
class ResearchContext:
    company: CompanyProfile
    metrics: FinancialMetrics
    price_statistics: PriceStatistics
    period: str
