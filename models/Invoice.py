
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric
from datetime import datetime
from sqlalchemy.orm import relationship

from database.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True)
    currency = Column(String(3), nullable = False)
    amount = Column(Numeric(10, 2), nullable = False)
    converted_amount = Column(Numeric(10, 2), nullable = False)
    date_created = Column(DateTime, default=datetime.now())
    _metadata = Column('metadata', String(255))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="invoices")