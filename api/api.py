import os
from fastapi import FastAPI
from pydantic import BaseModel
from chat2 import process_message  
from fastapi.middleware.cors import CORSMiddleware

port = int(os.environ.get("PORT",8080))
api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a Pydantic model for the request payload
class ChatRequest(BaseModel):
    user_id: str
    message: str

# API endpoint to handle chat requests
@api.post("/chat")
async def chat_endpoint(chat_input: ChatRequest):
    user_id = chat_input.user_id
    message = chat_input.message

    # Set user_id and process the message using your chat.py script
    response = process_message(user_id, message)  # Add a function in chat.py that processes the message and returns the response

    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:api", host="0.0.0.0", port=port, log_level="info")
