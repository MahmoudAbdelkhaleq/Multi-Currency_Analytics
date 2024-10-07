import strawberry

from .schema import InvoiceType, InvoiceCreate
from service import InvoiceService
from database.database import get_db, SessionLocal
from fastapi import Depends
from schema.InvoiceSchema import InvoiceCreate as InvoiceCreateSchema
@strawberry.type
class Mutation:
    def __init__(self):
        pass

    @strawberry.mutation
    async def create_Invoice(self, invoice: InvoiceCreate) -> InvoiceType:
        db = SessionLocal()  # Manually handle DB session here
        try:
            user_id=invoice.owner_id
            invoice = InvoiceCreateSchema(amount = invoice.amount, currency = invoice.currency, metadata = invoice.metadata)
            result = await InvoiceService.create_user_invoice(invoice=invoice, db=db, user_id=user_id)
            return result
        finally:
            db.close()
    
    @strawberry.mutation
    def delete_invoice(self, invoice_id: int) -> InvoiceType:
        db = SessionLocal()  # Manually handle DB session here
        try:
            return InvoiceService.delete_invoice(invoice_id=invoice_id, db=db)
        finally:
            db.close()
    
    @strawberry.mutation
    def update_invoice(self, invoice_id: int, invoice: InvoiceCreate) -> InvoiceType:
        db = SessionLocal()  # Manually handle DB session here
        try:
            return InvoiceService.update_invoice(invoice_id=invoice_id, invoice=invoice, db=db)
        finally:
            db.close()