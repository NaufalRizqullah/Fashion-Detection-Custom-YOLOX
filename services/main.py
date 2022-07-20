from fastapi import FastAPI
from pydantic import BaseModel

from services.api.api import main_router


class Item(BaseModel):
    name:str
    price: int
    discount: int

class ItemOutput(BaseModel):
    name: str
    selling_price: int

app = FastAPI()

app.include_router(main_router)

@app.get("/")
def root():
    return {"Message": "Welcome"}


@app.post("/itmes/", response_model=ItemOutput)
def add_item(item: Item):
    selling_price = item.price - item.discount
    return {
        "name": item.name,
        "selling_price": selling_price
    }