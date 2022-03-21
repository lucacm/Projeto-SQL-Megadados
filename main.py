from socket import create_server
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from sympy import product
from fastapi.encoders import jsonable_encoder

app = FastAPI()

market = {
    "carts":[
        {"id_cart" : 1, "id_user_fk" : 1, "product_fk_id" : []},
        {"id_cart" : 2, "id_user_fk" : 2, "product_fk_id" : []},
        {"id_cart" : 3, "id_user_fk" : 3, "product_fk_id" : []}
    ],
    "products":[
        {"id_prod" : 1, "name_prod" : "Melão", "description_prod" : "Fruta", "price_prod" : 6.5, "tax_prod" : 3.2},
        {"id_prod" : 2, "name_prod" : "Presunto", "description_prod" : "Frios", "price_prod" : 10.0, "tax_prod" : 2.0},
        {"id_prod" : 3, "name_prod" : "Papel Toalha", "description_prod" : "Limpeza", "price_prod" : 3.79, "tax_prod" : 4.5}
    ]
}

class Product_Add(BaseModel):
    id_prod: Optional[int] = None
    name_prod: str
    description_prod: Optional[str] = None
    price_prod: float
    tax_prod: Optional[float] = None

class Cart_Add(BaseModel):
    id_cart: Optional[int] = None
    id_user_fk: int
    product_fk_id: list = []
    
## ---------- PRODUTO ----------
@app.post("/products/", tags=["Produto"])
async def create_product(product: Product_Add):
    max_id = 0
    for item in market["products"]:
        if max_id < item["id_prod"]:
            max_id = item["id_prod"]
    max_id += 1
    product.id_prod = max_id
    update_product_encoded = jsonable_encoder(product)
    market["products"].append(update_product_encoded)
    return {
        "status": True,
        "message": "Product has been added successfully."
    }

@app.get("/products/", tags=["Produto"])
async def read_products():
    return market["products"]

@app.get("/products/{product_id}", tags=["Produto"])
async def read_product(product_id: int):
    for items in market["products"]:
        if items["id_prod"] == product_id:
            return items
    return {
        "status": False,
        "message": "Product was not found."
    }

@app.delete("/products/{product_id}", tags=["Produto"])
async def delete_item(product_id:int):
    for items in market["products"]:
        if items["id_prod"] == product_id:
            market["products"].remove(items)
            return {
                "status": True,
                "message": "Product was deleted successfully."
            }
    return {
        "status": False,
        "message": "Product was not found."
    }

@app.put("/products/{product_id}", tags=["Produto"])
async def update_item(product_id:int, product: Product_Add):
    for items in market["products"]:
        if items["id_prod"] == product_id:
            market["products"].remove(items)
            product.id_prod = product_id
            items = jsonable_encoder(product)
            print(items)
            market["products"].append(items)
            return {
                "status": True,
                "message": "Product was updated successfully."
            }
    return {
        "status": False,
        "message": "Product was not found."
    }

## ---------- CARRINHO ----------
@app.post("/carts/", tags=["Carrinho"])
async def create_cart(cart: Cart_Add):
    max_id = 0
    for item in market["carts"]:
        if max_id < item["id_cart"]:
            max_id = item["id_cart"]
    max_id += 1
    cart.id_cart = max_id
    update_cart_encoded = jsonable_encoder(cart)
    market["carts"].append(update_cart_encoded)
    return {
        "status": True,
        "message": "Cart has been created successfully."
    }

@app.get("/carts/", tags=["Carrinho"])
async def read_carts():
    return market["carts"]

@app.get("/carts/{carts_id}", tags=["Carrinho"])
async def read_cart(cart_id: int):
    for cart in market["carts"]:
        if cart["id_cart"] == cart_id:
            return cart
    return {
        "status": False,
        "message": "Cart was not found."
    }

@app.delete("/carts/{carts_id}", tags=["Carrinho"])
async def delete_cart(cart_id:int):
    for cart in market["carts"]:
        if cart["id_cart"] == cart_id:
            market["carts"].remove(cart)
            return {
                "status": True,
                "message": "Cart was deleted successfully."
            }
    return {
        "status": False,
        "message": "Cart was not found."
    }

@app.put("/carts/{carts_id}", tags=["Carrinho"])
async def update_item(cart_id:int, cart: Cart_Add):
    product_id_list = market["products"]
    for items in market["carts"]:
        if items["id_cart"] == cart_id:
            market["carts"].remove(items)
            cart.id_cart = cart_id
            cart_id_list = cart.product_fk_id
            cart.product_fk_id = []
            for list_id in cart_id_list:
                for i in product_id_list:
                    if i["id_prod"] == list_id:
                        print(i["id_prod"])
                        cart.product_fk_id.append(i["id_prod"])
                        break
            items = jsonable_encoder(cart)
            market["carts"].append(items)
            return {
                "status": True,
                "message": "Cart was updated successfully."
            }
    return {
        "status": False,
        "message": "Cart was not found."
    }