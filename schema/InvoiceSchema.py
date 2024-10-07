from typing import Union
from datetime import datetime

from pydantic import BaseModel


class InvoiceBase(BaseModel):
    currency: str
    amount : float
    _metadata : Union[str, None] = None


class InvoiceCreate(InvoiceBase):
    pass



class Invoice(InvoiceBase):
    id: int
    converted_amount: float
    date_created: datetime
    owner_id: int

    class Config:
        orm_mode = True
