from schemas import UserCreate
from sqlalchemy.orm import Session
from models import Users,Transactions
from schemas import TransactionCreate,Transaction

def create_user(db: Session, user: UserCreate):
    db_user = Users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def fetch_user(db:Session, user_id:int):
    return db.query(Users).filter(Users.id==user_id).first()

def update_user(db:Session,db_user:Users,user):
    db_user.username = user.username
    db_user.phone_number = user.phone_number
    db.commit()
    db.refresh(db_user)
    return db_user

def add_money(db: Session, user: Users, description: str, amount: float):
    balance = user.balance + amount
    user.balance =balance
    db.commit()
    db.refresh(user)
    create_transaction(db, user, description, amount)
    return {"user_id": user.id,
            "new_balance": user.balance,
            "last_updated": user.updated_at}

def withdraw(db: Session, user: Users, description: str, amount: float):
    if user.balance < amount:
        return {"error": "Insufficient funds"}
    balance = user.balance - amount
    user.balance = balance
    db.commit()
    db.refresh(user)
    create_transaction(db, user, description, -amount)  
    return {"user_id": user.id,
            "new_balance": user.balance,
            "description": description,
            "last_updated": user.updated_at}

def create_transaction(db: Session, user: Users, description: str, amount: float):
    transaction = TransactionCreate(user_id=user.id, description=description, amount=amount)
    new_transaction = Transactions(**transaction.dict())
    if transaction.amount < 0:
        new_transaction.transaction_type = "withdrawal"
    else:
        new_transaction.transaction_type = "deposit"
    new_transaction.user_id = user.id
    new_transaction.recipient_id = user.id
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

def fetch_transactions(db: Session, user_id: int):
    return db.query(Transactions).filter(Transactions.user_id == user_id).all()

