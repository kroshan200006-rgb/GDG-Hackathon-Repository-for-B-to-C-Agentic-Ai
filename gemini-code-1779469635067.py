from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from stylist_agent import StyleAgent

app = FastAPI(
    title="Lucknow AI Stylist API",
    description="D2C personalized ethnic wear recommendation engine.",
    version="1.0.0"
)

# Initialize the AI Agent
agent = StyleAgent()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    recommendation: str

@app.get("/")
def health_check():
    return {"status": "Active", "message": "Lucknow AI Stylist is running smoothly."}

@app.post("/chat", response_model=ChatResponse)
def chat_with_stylist(request: ChatRequest):
    \"\"\"
    Send a message to the AI stylist with occasion, budget, and preferences.
    \"\"\"
    try:
        reply = agent.get_recommendation(request.message)
        return ChatResponse(recommendation=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendation: {str(e)}")