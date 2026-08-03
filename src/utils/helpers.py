def format_market_cap(value):

    if not value:
        return "N/A"

    if value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f} T"

    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f} B"

    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f} M"

    return f"${value:,.0f}"