from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

router = APIRouter()

@router.post("/book")
def book_appointment(
    patient_id: int,
    doctor_id: int,
    appointment_date: str,
    notes: str = "",
    db: Session = Depends(get_db)
):
    db.execute(text("""
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, notes)
        VALUES (:patient_id, :doctor_id, :appointment_date, 'pending', :notes)
    """), {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "appointment_date": appointment_date,
        "notes": notes
    })
    db.commit()
    return {"message": "Appointment booked successfully!"}

@router.get("/all")
def get_all_appointments(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM appointments")).fetchall()
    return {"appointments": [dict(row._mapping) for row in result]}

@router.get("/{patient_id}")
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    result = db.execute(text(
        "SELECT * FROM appointments WHERE patient_id = :id"), {"id": patient_id}).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="No appointments found")
    return {"appointments": [dict(row._mapping) for row in result]}

@router.put("/update/{appointment_id}")
def update_appointment(appointment_id: int, status: str, db: Session = Depends(get_db)):
    db.execute(text(
        "UPDATE appointments SET status = :status WHERE id = :id"),
        {"status": status, "id": appointment_id})
    db.commit()
    return {"message": "Appointment updated successfully!"}