from src.services.stock_service import StockService


def test_company_lookup():

    service = StockService()

    result = service.get_company_info("MSFT")

    assert result["name"] is not None