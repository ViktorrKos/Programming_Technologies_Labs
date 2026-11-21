# catalog_service.py
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Catalog Service")

# База даних товарів каталогу
CATALOG = {
    1: {"name": "iPhone 16 Pro", "category": "Гаджети", "price": 1200.0, "in_stock": True},
    2: {"name": "Куртка", "category": "Одяг", "price": 150.0, "in_stock": True},
    3: {"name": "Телевізор", "category": "Техніка", "price": 800.0, "in_stock": False}
}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Отримання інформації про товар за ID"""
    if item_id not in CATALOG:
        raise HTTPException(status_code=404, detail="Товар не знайдено в каталозі")
    return CATALOG[item_id]