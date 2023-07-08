from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat import process_message
from typing import Union, List, Optional
import logging

# import utils
from utils import (storage, password_manager)

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

class RegisterInput(BaseModel):
    user_id: str   # User needs to input username
    password: str # User needs to input password

class RegisterOutput(BaseModel):
    message: str    # This will output a message

class MessageInput(BaseModel):
    user_id: str
    password: Optional[str]=None
    message: str

class MessageOutput(BaseModel):
    response: Union[str, List[str]]

@api.post("/register", response_model=RegisterOutput)
def register_endpoint(register_input: RegisterInput) -> RegisterOutput:
    user_id = register_input.user_id
    user_password = register_input.password

    if storage.check_user_exits(user_id):
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        hashed_pwd = password_manager.generate_password_hash(user_password)

        # Save initial user data
        storage.save_user(user_id, hashed_pwd)
        
        return RegisterOutput(message=f"Your user account has been created.")

@api.post("/message", response_model=MessageOutput)
def process_message_endpoint(message_input: MessageInput) -> MessageOutput:
    user_id = message_input.user_id
    user_password = message_input.password
    user_message = message_input.message

    logger.info(f"Received message from user {user_id}: {user_message}")

    if not storage.check_user_exits(user_id):
        return HTTPException(status_code=400, response="User does not exist. Please register first.")
    else:
        logger.info(f"Checking password for user {user_id} with entered password: {user_password}")
        if not password_manager.check_password(user_id, user_password):
            raise HTTPException(status_code=400, detail="Invalid password. Please try again.")

    try:
        # Call the process_message function with the user_input and get the response
        res = process_message(user_id, user_password, user_message)
        logger.info(f"Received response from process_message: {res}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise

    logger.info(f"Sending response: {res}")

    # Return the response as JSON
    return MessageOutput(response=res)