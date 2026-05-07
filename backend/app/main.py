from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from api import auth, patients, appointments, health_records, chat

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Healthcare Chatbot API",
    description="AI-Powered Healthcare Chatbot with EHR Integration",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(health_records.router, prefix="/health-records", tags=["Health Records"])
app.include_router(chat.router, prefix="/chat", tags=["Healthcare Chatbot"])

@app.get("/")
def root():
    return {"message": "Healthcare Chatbot API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}