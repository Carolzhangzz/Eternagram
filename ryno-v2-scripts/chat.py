# import from utils.py
from utils import (storage, password_manager, openai_api, vdb, timestamp_to_datetime)

# import other essentials
from dotenv import load_dotenv
import time
from uuid import uuid4
import json

# import scenes
from scenes.prologue import prologue
from scenes.scene1 import scene1, scene1_trigger,scene1_animation
from scenes.scene2 import scene2, scene2_trigger, scene2_animation
from scenes.scene3 import scene3

load_dotenv()

# MODELS
GPT3_MODEL = 'gpt-3.5-turbo'
GPT4_MODEL = 'gpt-4'
    
# FUNCTION: PROCESS MESSAGE
def process_message(user_id, entered_password, message):
    total_start_time = time.time()

    # [Check user existence and password validation]
    if not storage.check_user_exits(user_id):  
        return "User does not exist. Please register first."
    elif password_manager.check_password(user_id, entered_password) == False:
        return "Invalid password. Please try again."

    # Get user input, save it, vectorize it, save to pinecone
    payload = list()
    timestamp = time.time()
    timestring = timestamp_to_datetime(timestamp)
    vector_start_time = time.time()
    vector = openai_api.gpt3_embeddings(message)
    print(f"Vector generation for user input took {time.time() - vector_start_time} seconds")
    unique_id = str(uuid4())

    # Retrieve the latest conversation metadata
    metadata, latest_conversation_json = storage.get_latest_file(user_id)

    # Load latest step and scene
    if latest_conversation_json:
        latest_conversation = json.loads(latest_conversation_json)
        step = latest_conversation['step']
        scene = latest_conversation['scene']
    else:
        # If there's no previous conversation, start from the beginning
        step = 1
        scene = 'prologue'

    if scene == 'prologue':
        scene, res, next_step = prologue(message, step)
    elif scene == 'scene1':
        scene, res, next_step = scene1(message, user_id, vector, step)
        # Check for trigger word
        trigger_result = scene1_trigger(message)
        if trigger_result == "True":
            res = scene1_animation()
            scene = 'scene2'
    elif scene == 'scene2':
        scene, res, next_step = scene2(message, user_id, vector, step)
        # Check if the trigger word is found
        trigger_result = scene2_trigger(message)
        if trigger_result == "True":
            res = scene2_animation()
            scene = 'scene3'
    elif scene == 'scene3':
        res = scene3(message, user_id, vector)
    else:
        print("Invalid scene")
        return "You are in invalid scene"
    
    print(f"The scene is now {scene}, and step is now {step}")

    # update the next step and scene
    step = next_step

    # Save user message
    metadata = {'speaker': 'You', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id, 'user_id': user_id, 'step': step, 'scene': scene}
    storage.save_json('path/to/nexus/%s/%s.json' % (user_id, unique_id), metadata)
    payload.append((unique_id, vector, metadata))

    # Check if the response is a list or not
    if isinstance(res, list):
        res_vector = "\n".join(res)
    else:
        res_vector = res

    # Save Ryno's response, vectorize, save, etc
    timestamp = time.time()
    timestring = timestamp_to_datetime(timestamp)
    message = res_vector
    vector_start_time = time.time()
    vector = openai_api.gpt3_embeddings(res_vector)
    print(f"Vector generation for response took {time.time() - vector_start_time} seconds")
    unique_id = str(uuid4())
    metadata = {'speaker': 'Ryno', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id, 'user_id': user_id, 'step': step, 'scene': scene}
    storage.save_json('path/to/nexus/%s/%s.json' % (user_id, unique_id), metadata)
    payload.append((unique_id, vector, metadata))
    vdb.upsert(payload)

    print(f"Total time: {time.time() - total_start_time} seconds")

    return res
