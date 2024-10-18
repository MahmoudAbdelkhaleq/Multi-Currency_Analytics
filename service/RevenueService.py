from sqlalchemy.orm import Session

from utils import api_conversions
from typing import Union
from datetime import datetime
from .InvoiceService import get_invoices_by_user, get_invoices_by_user_within_period

async def get_total_revenue_in_currency(db: Session, user_id: int, currency: Union[str,None] = 'USD'):
    invoices = get_invoices_by_user(db, user_id)
    revenue_in_USD = sum([invoice.converted_amount for invoice in invoices])
    revenue_in_currency = await api_conversions.get_amount_in_currency_from_usd(revenue_in_USD, currency)
    return revenue_in_currency


async def get_total_revenue_per_currency(db: Session, user_id: int):
    invoices = get_invoices_by_user(db, user_id)
    revenue_per_currency = {}
    for invoice in invoices:
        if invoice.currency not in revenue_per_currency:
            revenue_per_currency[invoice.currency] = 0
        revenue_per_currency[invoice.currency] += invoice.amount
    return revenue_per_currency

# average revenue related functions

async def get_average_revenue_in_currency(db: Session, user_id: int, currency: Union[str, None] = 'USD'):
    invoices = get_invoices_by_user(db, user_id)
    revenue_in_USD = sum([invoice.converted_amount for invoice in invoices])
    revenue_in_currency = await api_conversions.get_amount_in_currency_from_usd(revenue_in_USD, currency)
    return revenue_in_currency / len(invoices)

async def get_average_revenue_per_currency(db: Session, user_id: int):
    invoices = get_invoices_by_user(db, user_id)
    revenue_per_currency = {}
    invoices_count_per_currency = {}
    for invoice in invoices:
        if invoice.currency not in revenue_per_currency:
            revenue_per_currency[invoice.currency] = 0
            invoices_count_per_currency[invoice.currency] = 0
        revenue_per_currency[invoice.currency] += invoice.amount
        invoices_count_per_currency[invoice.currency] += 1
    for currency in revenue_per_currency:
        revenue_per_currency[currency] /= invoices_count_per_currency[currency]
    return revenue_per_currency

# revenue trend related functions
async def get_revenue_trend_by_month(db: Session, user_id: int, currency: Union[str, None] = 'USD', year: int = datetime.now().year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31, 23, 59, 59)
    invoices = get_invoices_by_user_within_period(db, user_id, start_date, end_date)
    revenue_trend = {}
    for month_num in range(1, 13):
        month = api_conversions.get_month_name(month_num)
        revenue_trend[month] = 0
    for invoice in invoices:
        month = api_conversions.get_month_name(invoice.date_created.month)
        revenue_trend[month]+=invoice.converted_amount
    for month in revenue_trend:
        revenue_trend[month] = await api_conversions.get_amount_in_currency_from_usd(revenue_trend[month], currency)
    return revenue_trend