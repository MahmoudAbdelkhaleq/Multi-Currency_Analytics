from sqlalchemy.orm import Session


from schema.InvoiceSchema import InvoiceCreate, InvoiceUpdate
from utils import api_conversions
from repositories import InvoiceRepository
from datetime import datetime
from models.Invoice import Invoice

def get_invoices(db: Session, skip: int = 0, limit: int = 20):
    return InvoiceRepository.get_invoices(db, skip, limit)

async def create_user_invoice(db: Session, invoice: InvoiceCreate, user_id: int):
    converted_amount = await api_conversions.get_converted_amount_to_usd(invoice.amount, invoice.currency)
    db_invoice = Invoice(**invoice.model_dump(), owner_id=user_id, converted_amount=converted_amount)
    return InvoiceRepository.create_user_invoice(db, db_invoice)

def get_invoice(db: Session, invoice_id: int):
    return InvoiceRepository.get_invoice(db, invoice_id)

def get_invoices_by_user(db: Session, user_id: int):
    return InvoiceRepository.get_invoices_by_user(db, user_id)

def get_invoices_by_user_within_period(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return InvoiceRepository.get_invoices_by_user_within_period(db, user_id, start_date, end_date)

async def update_invoice(db: Session, invoice_id: int, invoice: InvoiceUpdate):
    converted_amount = await api_conversions.get_converted_amount_to_usd(invoice.amount, invoice.currency)
    return InvoiceRepository.update_invoice(db, invoice_id, invoice, converted_amount)

def delete_invoice(db: Session, invoice_id: int):
    return InvoiceRepository.delete_invoice(db, invoice_id)
