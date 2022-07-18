from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name:str
    price: int
    discount: int

class ItemOutput(BaseModel):
    name: str
    selling_price: int

app = FastAPI()

@app.get("/")
async def root():
    return {"Message": "Welcome"}


@app.post("/itmes/", response_model=ItemOutput)
async def add_item(item: Item):
    selling_price = item.price - item.discount
    return {
        "name": item.name,
        "selling_price": selling_price
    }