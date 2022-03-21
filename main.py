from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from sympy import product

app = FastAPI()


# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: Optional[str] = None


class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


fake_items_db = [
        {"username": "luca", "password" : "luis", "email" : "luisluca@luis.com"},
        {"username": "luis", "password" : "luca", "email" : "lucaluis@luca.com"} 
    ]



products = list()

@app.post("/products/")
async def create_product(product: Product):
    products.append(product)
    return {
        "status": True,
        "message": "Product has been added successfully."
    }
    # return product

@app.get("/products/")
async def read_products():
    return products

@app.get("/products/{product_id}")
async def read_product(product_id: int):
    for dict in products:
        for key in dict:
            if key[0] == "id":
                if key[1] == product_id:
                    return dict
    return {
        "status": False,
        "message": "Product was not found."
    }

@app.delete("/products/{product_id}")
async def delete_item(product_id:int):
    for dict in products:
        for key in dict:
            if key[0] == "id":
                if key[1] == product_id:
                    products.remove(dict)
                    return {
                        "status": True,
                        "message": "Product was deleted successfully."
                    }
    return {
        "status": False,
        "message": "Product was not found."
    }
