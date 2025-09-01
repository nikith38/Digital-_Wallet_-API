from sqlalchemy import String, Integer, Column, Float,DateTime
from db import Base
from datetime import datetime

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username=Column(String(50),unique=True,nullable=False)
    email=Column(String(100),unique=True,nullable=False)
    password=Column(String(255),nullable=False)
    phone_number=Column(String(15))
    balance=Column(Float(2),default=0.0)
    created_at=Column(DateTime,default=datetime.now)
    updated_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)

class Transactions(Base):
    __tablename__ = "transactions"
    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer,nullable=False,foreign_key="users.id")
    transaction_type=Column(String(20),nullable=False)
    amount=Column(Float(2),nullable=False)
    description=Column(String(255))
    reference_transaction_id=Column(Integer,foreign_key="transactions.id")
    recipient_id=Column(Integer,nullable=False,foreign_key="users.id")
    created_at=Column(DateTime,default=datetime.now)



