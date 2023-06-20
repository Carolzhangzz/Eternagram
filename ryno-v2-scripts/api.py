import os
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from chat import process_message  
from fastapi.middleware.cors import CORSMiddleware

port = int(os.environ.get("PORT",8080))
api = FastAPI()
connected_clients = set()

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

async def get_next_user_input(websocket: WebSocket):
    user_input = await websocket.receive_text()
    return user_input

async def send_response_to_frontend(res: str, websocket: WebSocket):
    await websocket.send_text(res)

@api.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)

    # Receive the user_id from the frontend
    user_id = await get_next_user_input(websocket)

    try:
        while True:
            user_input = await get_next_user_input(websocket)
            print(f"User: {user_input}")

            # Call process_message() with the user_input and get the response
            res = await process_message(user_id, user_input, websocket, get_next_user_input)

            # Send the response to the frontend
            await send_response_to_frontend(res, websocket)
    finally:
        connected_clients.remove(websocket)
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:api", host="0.0.0.0", port=port, log_level="info")
