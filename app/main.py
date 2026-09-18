from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.agent import run_agent
from agent.memory import clear_history


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "Agentic ML Chatbot API is running!"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    response = run_agent(request.message)

    return {
        "user_message": request.message,
        "response": response
    }


@app.post("/clear-memory")
def clear_chat_memory():

    clear_history()

    return {
        "message": "Conversation memory cleared."
    }