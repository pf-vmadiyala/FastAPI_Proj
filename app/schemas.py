"""
schemas.py — WHAT THE API SENDS/RECEIVES AS JSON (API layer)

Mental model:
  Client  ↔  THIS FILE  ↔  app.py  ↔  models.py  ↔  MySQL

  Pydantic checks types before your route logic runs.
  Wrong JSON → 422 error, never hits the database.
"""

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    """
    Incoming body for POST /product.

    No `id` here — client does not choose id; MySQL AUTO_INCREMENT does after insert.
    """

    name: str
    description: str
    price: float
    quantity: int


class ProductRead(BaseModel):
    """
    Outgoing JSON for GET/POST responses.

    from_attributes=True means: "I can be built from a SQLAlchemy object"
      e.g. db_product.name, db_product.id — not only from a plain dict.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price: float
    quantity: int
