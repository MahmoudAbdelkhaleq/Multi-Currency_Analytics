from datetime import timedelta, datetime, timezone

import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Union, Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import uvicorn
import sys
import os


# Get the directory of the current file
current_directory = os.getcwd()

# Add the directory to the system path
if current_directory not in sys.path:
    sys.path.append(current_directory)

print("Current directory added to system path:", current_directory)
from utils import api_conversions


from database.database import get_db, engine, Base
from datetime import datetime

from schema.UserSchema import UserCreate, UserUpdate, User
from schema.InvoiceSchema import InvoiceCreate, Invoice
from service import InvoiceService, UserService, RevenueService


from graphQL.Query import Query as query
from graphQL.Mutation import Mutation as mutation

from models.Token import Token

Base.metadata.create_all(bind=engine)


app = FastAPI()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = UserService.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# User CRUD

@app.post("/users/", response_model = User)
def create_user(user: UserCreate, db: Session = Depends(get_db))->User:
    db_user = UserService.get_user_by_email(db = db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = UserService.get_user_by_username(db = db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return UserService.create_user(db = db, user=user)

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(UserService.get_current_active_user)):
    return current_user

# @app.get("/users/me/invoices/")
# async def read_invoices_me(current_user: User = Depends(UserService.get_current_active_user), db: Session = Depends(get_db)):
#     invoices = await InvoiceService.get_invoices_by_user(db = db, user_id=current_user.id)
#     return invoices

@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    users = UserService.get_users(db = db, skip=skip, limit=limit)
    return users

@app.put("/users/{user_id}", response_model=UserUpdate)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = UserService.update_user(db = db, user_id=user_id, user=user)
    return db_user

@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserService.delete_user(db = db, user_id=user_id)
    return db_user

@app.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserService.get_user(db = db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Invoice CRUD

@app.post("/invoices/{user_id}/", response_model=Invoice)
async def create_invoice_for_user(
    user_id: int, invoice: InvoiceCreate, db: Session = Depends(get_db)
):
    created_invoice = await InvoiceService.create_user_invoice(db = db, invoice=invoice, user_id=user_id)
    return created_invoice


@app.get("/invoices/", response_model=List[Invoice])
def read_invoices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    invoices = InvoiceService.get_invoices(db = db, skip=skip, limit=limit)
    return invoices

@app.get("/invoice/{invoice_id}", response_model=Invoice)
def read_invoice(invoice_id: int, db: Session = Depends(get_db)):
    db_invoice = InvoiceService.get_invoice(db = db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return db_invoice

@app.get("/invoices/{user_id}", response_model=List[Invoice])
def get_invoices_by_user(user_id: int, db: Session = Depends(get_db)):
    db_invoices = InvoiceService.get_invoices_by_user(db = db, user_id=user_id)
    if db_invoices is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return db_invoices

@app.put("/invoices/", response_model=Invoice)
async def update_invoice(invoice_id: int, invoice: InvoiceCreate, db: Session = Depends(get_db)):
    db_invoice = await InvoiceService.update_invoice(db = db, invoice_id=invoice_id, invoice=invoice)
    return db_invoice
 

@app.delete("/invoices/{invoice_id}", response_model=Invoice)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    db_invoice = InvoiceService.delete_invoice(db = db, invoice_id=invoice_id)
    return db_invoice


#exchange rate endpoint
@app.get("/exchange_rate/{currency}")
async def get_exchange_rate(currency: str):
    exchange_rate = await api_conversions.get_exchange_rate(currency)
    return {"Currency": currency,
            "Standard Currency": 'USD',
            "Exchange Rate": exchange_rate}

# Additional endpoints for Anaylitics



@app.get("/total_revenue_per_currency/{user_id}/")
async def total_revenue_per_currency(user_id: int,  db: Session = Depends(get_db)):
    revenue = await RevenueService.get_total_revenue_per_currency(db = db, user_id=user_id)
    return revenue

@app.get("/total_revenue_in_currency/{user_id}/")
async def total_revenue_in_currency(user_id: int, currency: Union[str, None] = Query(default = 'USD'), db: Session = Depends(get_db)):
    revenue = await RevenueService.get_total_revenue_in_currency(db = db, user_id=user_id, currency = currency)
    return {'revenue': revenue}

@app.get("/revenue_trend/{user_id}/")
async def get_revenue_trend_by_month(user_id: int, year:int = datetime.now().year, currency:Union[str,None] = Query(default = 'USD'), db: Session = Depends(get_db)):
    revenue = await RevenueService.get_revenue_trend_by_month(db = db, user_id=user_id, currency = currency, year = year)
    return revenue


schema = strawberry.Schema(query=query, mutation=mutation)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

# This ensures the server runs only if the script is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)