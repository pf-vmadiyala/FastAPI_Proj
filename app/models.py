"""
models.py — WHAT THE MYSQL TABLE LOOKS LIKE (database layer)

Mental model:
  Client JSON  →  schemas.py  →  THIS FILE  →  db.py  →  MySQL

  Product here is NOT the same as ProductCreate in schemas.py:
    - schemas = API contract (what JSON looks like)
    - models  = table shape (what rows in `products` look like)

  __tablename__ = "products" is how SQLAlchemy knows:
    db.query(Product)  →  SELECT ... FROM products
"""

# models.py
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from db import Base


class Product(Base):
    """One row in the `products` table."""

    __tablename__ = "products"  # actual MySQL table name (not the Python class name)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1000))
    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(Integer)
