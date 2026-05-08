from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from groq import Groq
from prompts import get_system_prompt
import os

router = APIRouter()

conversation_histories = {}

client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

def chat_with_bot(message: str, history: list, patient_name: str, mode: str, language: str):
    history.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": get_system_prompt(patient_name, mode, language)}] + history,
        max_tokens=1000
    )
    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})
    return assistant_message, history

def analyze_sentiment(message: str):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a sentiment analyzer. Respond with only one word."},
            {"role": "user", "content": f"Analyze the urgency of this healthcare message in one word only (normal/concerned/urgent/emergency): '{message}'"}
        ],
        max_tokens=10
    )
    return response.choices[0].message.content.strip().lower()

@router.post("/message")
def send_message(
    patient_id: int,
    message: str,
    mode: str = "friendly",
    language: str = "english",
    db: Session = Depends(get_db)
):
    if patient_id not in conversation_histories:
        conversation_histories[patient_id] = []

    patient = db.execute(text("SELECT full_name FROM patients WHERE id = :id"), {"id": patient_id}).fetchone()
    patient_name = patient.full_name if patient else "Patient"

    sentiment = analyze_sentiment(message)

    response, conversation_histories[patient_id] = chat_with_bot(
        message,
        conversation_histories[patient_id],
        patient_name,
        mode,
        language
    )

    db.execute(text("""
        INSERT INTO chat_logs (patient_id, message, response, sentiment)
        VALUES (:patient_id, :message, :response, :sentiment)
    """), {
        "patient_id": patient_id,
        "message": message,
        "response": response,
        "sentiment": sentiment
    })
    db.commit()

    return {
        "response": response,
        "sentiment": sentiment,
        "patient_name": patient_name,
        "mode": mode,
        "language": language
    }

@router.get("/history/{patient_id}")
def get_chat_history(patient_id: int, db: Session = Depends(get_db)):
    result = db.execute(text(
        "SELECT * FROM chat_logs WHERE patient_id = :id ORDER BY created_at DESC"
    ), {"id": patient_id}).fetchall()
    return {"chat_history": [dict(row._mapping) for row in result]}

@router.delete("/clear/{patient_id}")
def clear_conversation(patient_id: int):
    if patient_id in conversation_histories:
        conversation_histories[patient_id] = []
    return {"message": "Conversation cleared!"}