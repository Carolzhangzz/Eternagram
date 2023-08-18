# import from utils.py
from utils import (storage, password_manager, openai_api, vdb, timestamp_to_datetime, get_last_response)

# import other essentials
from dotenv import load_dotenv
import time
from uuid import uuid4
import json

# import scenes
from scenes.prologue import prologue
from scenes.scene1 import scene1, scene1_trigger, scene1_animation
from scenes.scene2 import scene2, scene2_trigger, scene2_animation, scene2_animation2
from scenes.scene3 import scene3
from scenes.beliefs import run_scene2_questions

load_dotenv()

# MODELS
GPT3_MODEL = 'gpt-3.5-turbo'
GPT4_MODEL = 'gpt-4'
    
# FUNCTION: PROCESS MESSAGE
def process_message(user_id, entered_password, message):

    # [Check user existence and password validation]
    if not storage.check_user_exits(user_id):  
        return "User does not exist. Please register first."
    elif password_manager.check_password(user_id, entered_password) == False:
        return "Invalid password. Please try again."

    # [Get user input, save it, vectorize it, save to pinecone]
    payload = list()
    timestamp = time.time()
    timestring = timestamp_to_datetime(timestamp)
    vector = openai_api.gpt3_embeddings(message)
    unique_id = str(uuid4())

    # [Retrieve the latest conversation metadata]
    metadata, latest_conversation_json = storage.get_latest_file(user_id)

    # [Load latest step, scene, and start_time]
    if latest_conversation_json:
        latest_conversation = json.loads(latest_conversation_json)
        step = latest_conversation['step']
        scene = latest_conversation['scene']
        start_time = latest_conversation.get('start_time', time.time()) # default to current time if not found
    else:
        # [If there's no previous conversation, start from the beginning]
        step = 1
        scene = 'prologue'
        start_time = time.time() # record the start time of the conversation

    if scene == 'prologue':
        scene, res, next_step = prologue(message, step)
    elif scene == 'scene1':
        scene, res, next_step = scene1(message, user_id, vector, step, start_time)

        # [Check if the scene is advanced due to timeout]
        if scene == 'scene2':
            start_time = time.time()

        # [Check if the trigger word is found]
        trigger_result = scene1_trigger(message)
        if trigger_result == "True":
            res = scene1_animation()
            scene = 'scene2'
            start_time = time.time() # reset the start time when moving to the next scene
    elif scene == 'scene2':
        scene, res, next_step = scene2(message, user_id, vector, step, start_time)
        # [Check if the trigger word is found]
        last_response = get_last_response(user_id)
        trigger_result = scene2_trigger(message, last_response)
        if trigger_result == "True":
            res = scene2_animation()
            scene = 'scene2_animation'
    elif scene == 'scene2_animation':
        res = scene2_animation2()
        scene = 'scene2_questions'
        # scene = 'scene3'
        next_step = 5
    elif scene == 'scene2_questions':
        # Take the response as dictionary
        scene, response_obj, next_step = run_scene2_questions(step)

        # Obtain both question and possible choices
        question = response_obj["question"]
        choices = response_obj["responses"]

        # Return question and choices to the frontend
        if next_step >= 14:
            scene = 'scene3'
        res = {"question": question, "choices": choices}
    elif scene == 'scene3':
        res, next_step = scene3(step)
    else:
        print("Invalid scene")
        return "You are in invalid scene"
    
    print(f"The scene is now {scene}, and step is now {step}")

    # [Update the next step and scene]
    step = next_step

    # [Save user message]
    metadata = {'speaker': 'You', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id, 'user_id': user_id, 'step': step, 'scene': scene, 'start_time': start_time}
    storage.save_json('path/to/nexus/%s/%s.json' % (user_id, unique_id), metadata)
    payload.append((unique_id, vector, metadata))

    # [Check if the response is a list or dictionary or not]
    if isinstance(res, list):
        res_vector = "\n".join(res)
    elif isinstance(res, dict):
        res_vector = res.get("question")
        if res_vector is None:
            print("Key 'question' not found in dictionary 'res'")
            res_vector = "None"  # You'll need to set a suitable default value
    else:
        res_vector = message

    # [Save Ryno's response, vectorize, save, etc]
    timestamp = time.time()
    timestring = timestamp_to_datetime(timestamp)
    message = res_vector
    vector = openai_api.gpt3_embeddings(res_vector)
    unique_id = str(uuid4())
    metadata = {'speaker': 'Ryno', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id, 'user_id': user_id, 'step': step, 'scene': scene}
    storage.save_json('path/to/nexus/%s/%s.json' % (user_id, unique_id), metadata)
    payload.append((unique_id, vector, metadata))
    vdb.upsert(payload)

    return res
