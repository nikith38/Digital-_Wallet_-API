from fastapi import FastAPI,HTTPException,Depends
from db import engine,Base,get_db
import crud
from schemas import UserCreate,UserUpdate

Base.metadata.create_all(bind=engine)

app=FastAPI()   

@app.get("/")
def home():
    return {"message": "Welcome to the Digital Wallet API!"}

@app.get("/users/{user_id}")
def get_user(user_id: int,db=Depends(get_db)):
    user = crud.fetch_user(db, user_id)
    if user:
        return {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number,
            "balance": user.balance,
            "created_at": user.created_at
        }
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users/")
def create_user(user: UserCreate, db=Depends(get_db)):
    #print(user.dict())
    db_user = crud.create_user(db, user)
    return db_user


@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate, db=Depends(get_db)):
    db_user = crud.fetch_user(db, user_id)
    if db_user:
       crud.update_user(db, db_user,user)
       return db_user
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/wallet/{user_id}/balance")
def get_balance(user_id: int, db=Depends(get_db)):
    user = crud.fetch_user(db, user_id)
    if user:
        return {"user_id": user.id,
                "balance": user.balance,
                "last_updated": user.updated_at}
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/wallet/{user_id}/add-money")
def add_money(user_id: int, amount: float, description: str, db=Depends(get_db)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    user = crud.fetch_user(db, user_id)
    if user:
        return crud.add_money(db, user, description, amount)
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/wallet/{user_id}/withdraw")
def withdraw(user_id: int, amount: float, description: str, db=Depends(get_db)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    user = crud.fetch_user(db, user_id)
    if user:
        return crud.withdraw(db, user, description, amount)
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/transactions/{user_id}")
def get_transactions(user_id: int, db=Depends(get_db)):
    transactions = crud.fetch_transactions(db, user_id)
    if transactions:
        return transactions
    raise HTTPException(status_code=404, detail="No transactions found")

@app.get("/transactions/detail/{transaction_id}")
def get_transaction(transaction_id: int, db=Depends(get_db)):
    transaction = crud.fetch_transaction(db, transaction_id)
    if transaction:
        return transaction
    raise HTTPException(status_code=404, detail="Transaction not found")

@app.post("/transfer")
def transfer_funds(user_id: int, recipient_id: int, amount: float, description: str, db=Depends(get_db)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    user = crud.fetch_user(db, user_id)
    recipient = crud.fetch_user(db, recipient_id)
    if user and recipient:
        return crud.transfer_funds(db, user, recipient, amount, description)
    raise HTTPException(status_code=404, detail="User or recipient not found")

@app.post("/transfer/{transfer_id}")
def get_transfer(transfer_id: int, db=Depends(get_db)):
    transaction = crud.fetch_transaction(db, transfer_id)
    if transaction:
        return transaction
    raise HTTPException(status_code=404, detail="Transaction not found")