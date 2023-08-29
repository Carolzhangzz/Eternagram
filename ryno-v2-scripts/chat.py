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

# FUNCTION: MANAGE SCENES
def manage_scenes(scene, message, user_id, vector, step):
    """Manage scenes based on the current scene."""
    if scene == 'prologue':
        return prologue(message, step)
    elif scene == 'scene1':
        return scene1(message, user_id, vector, step)
    elif scene == 'scene2':
        return scene2(message, user_id, vector, step)
    elif scene == 'scene2_animation':
        res = scene2_animation2()
        scene = 'scene2_questions'
        return scene, res, 5
    elif scene == 'scene2_questions':
        scene, response_obj, next_step = run_scene2_questions(step)

        # [Obtain both question and possible choices]
        question = response_obj["question"]
        choices = response_obj["responses"]

        # [Return question and choices to the frontend]
        if next_step >= 14:
            scene = 'scene3'
        res = {"question": question, "choices": choices}
        return scene, res, next_step
    elif scene == 'scene3':
        return scene3(step)
    else:
        print("Invalid scene")
        return "You are in invalid scene"
    
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
        print(f"The metadata is {latest_conversation}")
        step = latest_conversation['step']
        scene = latest_conversation['scene']
        start_time = latest_conversation.get('start_time', None) 
        print(f"Retrieved start_time: {start_time}")
    else:
        # [If there's no previous conversation, start from the beginning]
        step = 1
        scene = 'prologue'
        start_time = None

    # [Check if more than 5 mins have passed in scene1 or scene2]
    print(f"Current Scene: {scene}, Start time: {start_time}")
    if scene in ['scene1', 'scene2'] and start_time is not None:
        elapsed_time = time.time() - start_time 
        print(f"Checking elapsed time for {scene}. Current Time: {time.time()}, Start Time: {start_time}, Elapsed Time: {elapsed_time}")  # Print current time, start time, elapsed time
        if elapsed_time > 240:
            print(f"4 minutes passed in {scene}. Transitioning scene.")
            if scene == 'scene1':
                scene = 'scene2'
                res = scene1_animation()  # replace with appropriate method to transition from scene1 to scene2
                next_step = 5
            elif scene == 'scene2':
                scene = 'scene2_animation'
                res = scene2_animation()  # replace with appropriate method to transition from scene2 to scene2_animation
                next_step = 5
            start_time = time.time() # reset the start time for the new scene
            print(f"New {scene} started at {start_time}") # Print that new scene started
        else:
            # [Assign to temporary variables to avoid overriding the values prematurely]
            next_scene, res, next_step = manage_scenes(scene, message, user_id, vector, step)

            # [Check if trigger word is found in scene1]
            if scene == 'scene1':
                trigger_result = scene1_trigger(message)
                if trigger_result == "True":
                    res = scene1_animation()
                    scene = 'scene2'
                    next_step = 5
                else:
                    scene = next_scene
                    step = next_step
            # [Check if trigger word is found in scene2]
            elif scene == 'scene2':
                last_response = get_last_response(user_id)
                trigger_result = scene2_trigger(message, last_response)
                if trigger_result == "True":
                    res = scene2_animation()
                    scene = 'scene2_animation'
                    next_step = 5
                else:
                    scene = next_scene
                    step = next_step
    else:
        # [If scene is not either 'scene1' or 'scene2', follow the usual flow.]
        if scene != 'scene3':
            scene, res, next_step = manage_scenes(scene, message, user_id, vector, step)
        else:
            res, next_step = manage_scenes(scene, message, user_id, vector, step)

    # [Update the next step and scene]
    step = next_step

    print(f"The scene is {scene}, and the step is {step}")

    # [Save user message]
    metadata = {'speaker': 'You', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id, 'user_id': user_id, 'step': step, 'scene': scene}
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
        res_vector = res

    # [Save Ryno's response, vectorize, save, etc]
    timestamp = time.time()
    timestring = timestamp_to_datetime(timestamp)
    message = res_vector
    vector = openai_api.gpt3_embeddings(res_vector)
    unique_id = str(uuid4())
    metadata = {'speaker': 'Ryno', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id, 'user_id': user_id, 'step': step, 'scene': scene}

    # [Add start_time to metadata only at the beginning of scene1 or scene2]
    if (scene == 'scene1' and step == 4) or (scene == 'scene2' and step == 5): 
        print(f"I went here!") 
        # [Prevent resetting start_time for every request]
        if start_time is None:
            print("The start_time is None. Setting a new one.")
            start_time = time.time()

    # [Add the start time to metadata]
    if start_time is not None:
        metadata['start_time'] = start_time
        print(f"Set start_time: {metadata['start_time']}")
    
    storage.save_json('path/to/nexus/%s/%s.json' % (user_id, unique_id), metadata)
    saved_metadata = storage.load_json('path/to/nexus/%s/%s.json' % (user_id, unique_id))  # replace `storage.load_json` with the appropriate function to load the json file
    print(f"Saved metadata: {saved_metadata}")
    payload.append((unique_id, vector, metadata))
    vdb.upsert(payload)

    return res
