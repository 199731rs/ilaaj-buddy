from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime, timedelta
from jose import jwt
import hashlib

router = APIRouter()

SECRET_KEY = "healthcare_secret_key_2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain, hashed):
    return hashlib.sha256(plain.encode()).hexdigest() == hashed

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register")
def register(username: str, email: str, password: str, role: str, db: Session = Depends(get_db)):
    from sqlalchemy import text
    hashed = hash_password(password)
    db.execute(text("INSERT INTO users (username, email, password, role) VALUES (:u, :e, :p, :r)"),
               {"u": username, "e": email, "p": hashed, "r": role})
    db.commit()
    return {"message": "User registered successfully!"}

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    from sqlalchemy import text
    result = db.execute(text("SELECT * FROM users WHERE username = :u"), {"u": username}).fetchone()
    if not result or not verify_password(password, result.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": username, "role": result.role})
    return {"access_token": token, "token_type": "bearer"}