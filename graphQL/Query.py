import strawberry
from typing import List
from service import InvoiceService
from .schema import InvoiceType
from database.database import SessionLocal
from fastapi import Depends

@strawberry.type
class Query:

    @strawberry.field
    def hello(self) -> str:
        return "Hello, world!"

    @strawberry.field
    def get_all_invoices(self) -> List[InvoiceType]:
        db = SessionLocal()  # Manually handle DB session here
        try:
            return InvoiceService.get_invoices(skip = 0, limit = 20, db = db)
        finally:
            db.close()
    
    @strawberry.field
    def get_invoice_by_id(self, invoice_id: int) -> InvoiceType:
        db = SessionLocal()
        try:
            return InvoiceService.get_invoice(invoice_id = invoice_id, db = db)
        finally:
            db.close()