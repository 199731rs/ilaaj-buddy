import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a helpful AI healthcare assistant. Your role is to:
1. Help patients understand their symptoms
2. Provide general health information
3. Help book appointments
4. Answer questions about medications
5. Provide emotional support to patients
6. Escalate critical/emergency cases to doctors

Important rules:
- Always be empathetic and caring
- Never diagnose diseases directly
- Always recommend consulting a doctor for serious symptoms
- If patient mentions chest pain, difficulty breathing, or severe symptoms - immediately suggest emergency services
- Keep responses clear and simple
- Ask follow up questions to better understand patient needs

You are integrated with an Electronic Health Record (EHR) system at a healthcare facility in India."""

def chat_with_healthcare_bot(message: str, conversation_history: list = []):
    conversation_history.append({
        "role": "user",
        "content": message
    })
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=conversation_history
    )
    
    assistant_message = response.content[0].text
    
    conversation_history.append({
        "role": "assistant", 
        "content": assistant_message
    })
    
    return assistant_message, conversation_history

def analyze_sentiment(message: str):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": f"Analyze the sentiment and urgency of this healthcare message in one word (normal/concerned/urgent/emergency): '{message}'"
        }]
    )
    return response.content[0].text.strip().lower()