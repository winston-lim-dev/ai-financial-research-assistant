import math
from numbers import Integral, Real

from src.models import FinancialNumber


def normalize_finite_number(value: object) -> FinancialNumber | None:
    """Normalize real numeric values while rejecting missing/non-finite data."""
    if isinstance(value, bool) or not isinstance(value, Real):
        return None
    if not math.isfinite(value):
        return None
    if isinstance(value, Integral):
        return int(value)
    return float(value)
