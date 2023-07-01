from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat import process_message
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageInput(BaseModel):
    user_id: str
    message: str

class MessageOutput(BaseModel):
    response: str

@api.post("/message", response_model=MessageOutput)
def process_message_endpoint(message_input: MessageInput) -> MessageOutput:
    user_id = message_input.user_id
    user_message = message_input.message

    logger.info(f"Received message from user {user_id}: {user_message}")

    try:
        # Call the process_message function with the user_input and get the response
        res = process_message(user_id, user_message)
        logger.info(f"Received response from process_message: {res}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise

    logger.info(f"Sending response: {res}")

    # Return the response as JSON
    return MessageOutput(response=res)