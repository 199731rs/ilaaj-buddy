from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

router = APIRouter()

@router.post("/add")
def add_health_record(
    patient_id: int,
    doctor_id: int,
    diagnosis: str,
    prescription: str,
    test_results: str,
    visit_date: str,
    db: Session = Depends(get_db)
):
    db.execute(text("""
        INSERT INTO health_records (patient_id, doctor_id, diagnosis, prescription, test_results, visit_date)
        VALUES (:patient_id, :doctor_id, :diagnosis, :prescription, :test_results, :visit_date)
    """), {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "diagnosis": diagnosis,
        "prescription": prescription,
        "test_results": test_results,
        "visit_date": visit_date
    })
    db.commit()
    return {"message": "Health record added successfully!"}

@router.get("/all")
def get_all_records(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM health_records")).fetchall()
    return {"health_records": [dict(row._mapping) for row in result]}

@router.get("/{patient_id}")
def get_patient_records(patient_id: int, db: Session = Depends(get_db)):
    result = db.execute(text(
        "SELECT * FROM health_records WHERE patient_id = :id"), {"id": patient_id}).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="No health records found")
    return {"health_records": [dict(row._mapping) for row in result]}