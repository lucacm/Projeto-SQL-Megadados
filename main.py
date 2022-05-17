from socket import create_server
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from sympy import product
from fastapi.encoders import jsonable_encoder
from db import connection
from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String
from db import meta, engine
from starlette.status import HTTP_204_NO_CONTENT

# nome da database --> shopping
app = FastAPI()

produto = Table("produto", meta, Column("id_prod", Integer, primary_key=True), Column(
    "name_prod", String(255),), Column("description_prod", String(255)), Column("price_prod", String(255)), Column("tax_prod", String(255)))

carrinho = Table("carrinho", meta, Column("id_cart", Integer, primary_key=True), Column(
    "id_user_fk", String(255)), Column("produtos", String(255)))

meta.create_all(engine)


class Product_Add(BaseModel):
    id_prod: Optional[int]
    name_prod: str
    description_prod: Optional[str]
    price_prod: str
    tax_prod: str


class Cart_Add(BaseModel):
    id_cart: Optional[int]
    id_user_fk: int
    produtos: str


# ---------- PRODUTO ----------

@app.get("/products", tags=["Produto"])
async def read_products():
    return connection.execute(produto.select()).fetchall()


@app.get("/products/{product_id}", tags=["Produto"])
async def read_product(product_id: int):
    return connection.execute(produto.select().where(produto.c.id_prod == product_id)).first()


@app.post("/products/add", tags=["Produto"])
async def create_product(product: Product_Add):
    new_product = {"name_prod": product.name_prod, "description_prod": product.description_prod,
                   "price_prod": product.price_prod, "tax_prod": product.tax_prod}
    result = connection.execute(produto.insert().values(new_product))
    return connection.execute(produto.select().where(produto.c.id_prod == result.lastrowid)).first()


@app.put("/products/{product_id}", tags=["Produto"])
async def update_item(product_id: int, product: Product_Add):
    connection.execute(produto.update().values(name_prod=product.name_prod, description_prod=product.description_prod,
                       price_prod=product.price_prod, tax_prod=product.tax_prod).where(produto.c.id_prod == product_id))
    return connection.execute(produto.select().where(produto.c.id_prod == product_id)).first()


@app.delete("/products/{product_id}", tags=["Produto"], status_code=HTTP_204_NO_CONTENT)
async def delete_item(product_id: int):
    connection.execute(produto.delete().where(produto.c.id_prod == product_id))
    return connection.execute(produto.select().where(produto.c.id_prod == product_id)).first()


# ---------- CARRINHO ----------

@app.get("/carts/", tags=["Carrinho"])
async def read_carts():
    return connection.execute(carrinho.select()).fetchall()


@app.get("/carts/{carts_id}", tags=["Carrinho"])
async def read_cart(cart_id: int):
    return connection.execute(carrinho.select().where(carrinho.c.id_cart == cart_id)).first()


@app.post("/carts/add", tags=["Carrinho"])
async def create_cart(cart: Cart_Add):
    new_product = {"id_user_fk": cart.id_user_fk, "produtos": cart.produtos}
    result = connection.execute(carrinho.insert().values(new_product))
    return connection.execute(carrinho.select().where(carrinho.c.id_cart == result.lastrowid)).first()
 

@app.put("/carts/{carts_id}", tags=["Carrinho"])
async def update_item(cart_id: int, cart: Cart_Add):
    connection.execute(carrinho.update().values(
        id_user_fk=cart.id_user_fk, produtos=cart.produtos).where(carrinho.c.id_cart == cart_id))
    return connection.execute(carrinho.select().where(carrinho.c.id_cart == cart_id)).first()


@app.delete("/carts/{carts_id}", tags=["Carrinho"], status_code=HTTP_204_NO_CONTENT)
async def delete_cart(cart_id: int):
    connection.execute(carrinho.delete().where(carrinho.c.id_cart == cart_id))
    return connection.execute(carrinho.select().where(carrinho.c.id_cart == cart_id)).first()
