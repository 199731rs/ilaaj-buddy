from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

router = APIRouter()

@router.post("/add")
def add_patient(
    user_id: int,
    full_name: str,
    date_of_birth: str,
    gender: str,
    phone: str,
    address: str,
    blood_group: str,
    db: Session = Depends(get_db)
):
    db.execute(text("""
        INSERT INTO patients (user_id, full_name, date_of_birth, gender, phone, address, blood_group)
        VALUES (:user_id, :full_name, :dob, :gender, :phone, :address, :blood_group)
    """), {
        "user_id": user_id,
        "full_name": full_name,
        "dob": date_of_birth,
        "gender": gender,
        "phone": phone,
        "address": address,
        "blood_group": blood_group
    })
    db.commit()
    return {"message": "Patient added successfully!"}

@router.get("/all")
def get_all_patients(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM patients")).fetchall()
    return {"patients": [dict(row._mapping) for row in result]}

@router.get("/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM patients WHERE id = :id"), {"id": patient_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Patient not found")
    return dict(result._mapping)