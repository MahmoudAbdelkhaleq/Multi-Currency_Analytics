from sqlalchemy.orm import Session

from models.Invoice import Invoice
from schema.InvoiceSchema import InvoiceCreate
from datetime import datetime

from database.database import SessionLocal, get_db
from fastapi import Depends, Query


def get_invoices(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Invoice).offset(skip).limit(limit).all()


def create_user_invoice(db: Session, db_invoice: Invoice):
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_invoice(db: Session, invoice_id: int):
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()

def get_invoices_by_user(db: Session, user_id: int):
    return db.query(Invoice).filter(Invoice.owner_id == user_id).all()

def get_invoices_by_user_within_period(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return db.query(Invoice).filter(Invoice.owner_id == user_id, Invoice.date_created>=start_date,
                                                Invoice.date_created<=end_date).all()

def update_invoice(db: Session, invoice_id: int, invoice: InvoiceCreate, converted_amount: int):
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    for field, value in invoice.__dict__.items():
        if value is not None:
            setattr(db_invoice, field, value)  # Update the invoice field with the new value
    db_invoice.converted_amount = converted_amount
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def delete_invoice(db: Session, invoice_id: int):
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    db.delete(db_invoice)
    db.commit()
    return db_invoice