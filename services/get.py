from services.google_table import google_sheet
from config import prID, prName

class ProductService:
    def __init__(self):
        self.data = None
    def refresh(self):
        self.data = google_sheet()
    
    def get_products(self):
        return [{"id": p[prID], "name": p[prName]} for p in self.data]
    
    def get_product(self, product_id):
        for product in self.data:
            if product[prID] == product_id:
                return product

service = ProductService()