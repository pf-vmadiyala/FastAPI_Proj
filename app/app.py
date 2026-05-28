"""
app.py — ROUTES (orchestrator)

Request flow for POST:
  Client JSON
    → ProductCreate (schemas) validates input
    → Product (models) is the row we want in MySQL
    → db.add / commit / refresh (session from db.py)
    → ProductRead (schemas) shapes the JSON we send back

Request flow for GET /products:
  db.query(Product) → list of SQLAlchemy rows → returned as JSON
"""

from app.models import Product  # SQLAlchemy: maps to table `products`
from app.schemas import ProductCreate, ProductRead  # Pydantic: JSON in/out
from db import SessionLocal  # factory for one DB session per request
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

app = FastAPI()


@app.get("/hello")
def hello():
    return {"message": "Hellow World"}


# OLD in-memory list approach (before MySQL) — kept for reference
# products = [
#     Product(id=1, name="Phone", description="A smartPhone", price=699.90, quantity=50),
#     Product(id=4, name="laptop", description="A Good Laptop", price=1999.90, quantity=8),
#     Product(id=6, name="Pen", description="A Black Pen", price=9.90, quantity=100),
#     Product(id=9, name="Table", description="A Office Table", price=199.90, quantity=5),
#     Product(id=10, name="Monitor", description="Wide Monitor", price=299.79, quantity=8),
# ]


def get_db():
    """
    Dependency: open a DB session for this request, close it when done.

    yield db  → route runs with this session
    finally   → always close, even if route crashes
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    """
    GET all rows from MySQL table `products`.

    Product (models) tells SQLAlchemy which table.
    .all() runs SELECT and returns a list (empty list [] if table is empty).
    """
    products = db.query(Product).all()
    return products


# OLD get-by-id using in-memory list — kept for reference
# @app.get(f"/product/{id}")
# def get_product_by_id(id: int):
#     for product in products:
#         if product.id == id:
#             return product
#     return "Product Not Found"


@app.post("/product", response_model=ProductRead, status_code=201)
def add_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    """
    POST one product.

    product_in = validated JSON (schemas) — safe to use .name, .price, etc.
    """
    # Build a SQLAlchemy row object (still only in Python memory)
    db_product = Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        quantity=product_in.quantity,
    )

    # db.add = "remember this row for insert" (no SQL yet)
    db.add(db_product)

    # db.commit = actually run INSERT INTO products (...) in MySQL
    db.commit()

    # db.refresh = re-read row from DB (picks up auto-generated id, etc.)
    db.refresh(db_product)

    # FastAPI converts db_product → JSON using ProductRead (from_attributes)
    return db_product


# OLD post using in-memory list — kept for reference
# @app.post("/product/")
# def add_product(product: Product):
#     products.append(product)
#     return product

# OLD put — kept for reference
# @app.put(f"/product/{id}")
# def update_product(id: int, product: Product):
#     for i in range(len(products)):
#         if products[i].id == id:
#             product[i] = product
#             return "Product successfully Added"
#     return "No Product with ID found"

# OLD delete — kept for reference
# @app.delete(f"/product/{id}")
# def delete_product(id: int):
#     for p in products:
#         if p.id == id:
#             products.remove(p)
#             return "Product Removed Successfully"
#     return "Product Not Found"
