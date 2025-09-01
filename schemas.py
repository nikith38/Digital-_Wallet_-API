from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    username: str
    email: str
    phone_number: str
    balance: float
    created_at: str

class UserCreate(BaseModel):
    username: str
    email: str
    phone_number: str
    password:str
    balance: float 

class UserUpdate(BaseModel):
    username: str
    phone_number: str

class Transaction(BaseModel):
    id: int
    user_id: int
    description: str
    amount: float
    created_at: str

class TransactionCreate(BaseModel):
    user_id: int
    description: str
    amount: float