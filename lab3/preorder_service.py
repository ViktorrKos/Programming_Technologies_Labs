# preorder_service.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Preorder Service")

# Тимчасова база передзамовлень
PREORDERS = []
_order_counter = 1

class PreorderRequest(BaseModel):
    customer_name: str
    item_id: int
    quantity: int

@app.post("/preorders/", status_code=201)
def create_preorder(request: PreorderRequest):
    global _order_counter

    # Перевірка на виключення/негативний сценарій (валідація)
    if not request.customer_name.strip():
        raise HTTPException(status_code=400, detail="Ім'я клієнта не може бути порожнім")
    if request.quantity <= 0:
        raise HTTPException(status_code=400, detail="Кількість товару повинна бути більше 0")

    order = {
        "id": _order_counter,
        "customer": request.customer_name,
        "item_id": request.item_id,
        "quantity": request.quantity,
        "status": "CONFIRMED"
    }
    PREORDERS.append(order)
    _order_counter += 1
    return order

@app.get("/preorders/")
def get_preorders():
    return PREORDERS