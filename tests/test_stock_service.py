from src.services.stock_service import StockService

service = StockService()

company = service.get_company_info("fake123")

print(company)