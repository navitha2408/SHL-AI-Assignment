from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from chatbot import chat_with_bot
from dotenv import load_dotenv
import threading
import webbrowser

load_dotenv()

app = FastAPI(
    title="SHL Assessment Recommender",
    version="1.0"
)

# Prevent opening multiple tabs during reload
browser_opened = False

@app.on_event("startup")
async def startup_event():
    global browser_opened
    if not browser_opened:
        browser_opened = True
        threading.Timer(
            1,
            lambda: webbrowser.open("http://127.0.0.1:8000/docs")
        ).start()


# ---------- Request Models ----------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# ---------- Health Endpoint ----------

@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- Chat Endpoint ----------

@app.post("/chat")
def chat(request: ChatRequest):

    reply, recommendations, end = chat_with_bot(request.messages)

    return {
        "reply": reply,
        "recommendations": recommendations,
        "end_of_conversation": end
    }


# ---------- Run ----------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )