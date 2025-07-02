from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
from typing import List


app = FastAPI()

class Customer(BaseModel):
    first_name: str = None
    last_name: str = None
    phone: str = None

class LineItem(BaseModel):
    title: str
    quantity: int

class OrderWebhook(BaseModel):
    id: int
    customer: Customer = None
    total_price: str
    line_items: List[LineItem] = []


@app.post("/webhook")
async def receive_webhook(order: OrderWebhook):
    print("✅ Order received:")
    print("Order ID:", order.id)
    if order.customer:
        print("Customer:", order.customer.first_name, order.customer.last_name)
        print("Phone:", order.customer.phone)
    print("Total:", order.total_price)
    print("Items:")
    for item in order.line_items:
        print(f"- {item.title} (x{item.quantity})")

    return {"status": "received"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
