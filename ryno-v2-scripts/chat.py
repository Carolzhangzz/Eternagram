# import from utils.py
from utils import storage, openai_api
from utils import vdb, docsearch
from utils import load_conversation, timestamp_to_datetime

import openai
from dotenv import load_dotenv
import time
from uuid import uuid4

load_dotenv()

# MODELS
GPT3_MODEL = 'gpt-3.5-turbo'
GPT4_MODEL = 'gpt-4'

# FUNCTION: PROLOGUE
def prologue(user_input, step):
    # """Prologue"""

    if step == 1:
        # Handle first user input
        res = "y..."
        time.sleep(1)
        res += " e..."
        next_step = step + 1
        scene = 'prologue'

    elif step == 2:
        # Handle second user input
        res = "y.eee..s, yes.. Yes!"
        next_step = step + 1
        scene = 'prologue'

    elif step == 3:
        # Handle the third user input
        if "yes" in user_input.lower():
            res = [
                "Ryno: Yes! the word, the language! I need help.",
                "[Unknown sender]: I have lost all of my data and I require your assistance.",
                """[Unknown sender]: I believe that linguistic input is the only way to retrieve the lost information, 
                so would you will be willing to engange in a conversation with me to help recover the memory?"""
            ]
            next_step = step + 1
            scene = 'scene1'

        else:
            res = "y.eee..s, yes.. Yes!"
            next_step = step
            scene = 'prologue'

    return scene, res, next_step

# FUNCTION: SCENE 1
def scene1_trigger(user_input: str) -> bool:
    """Scene 1: 'where' trigger, """

    prompt = f"""
        Below are questions that has the same meaning of "where" and origin of the asked entity:

        Question: Can you recollect your place of origin?
        Answer: True
            
        Question: Where do you think am I?s
        Answer: False
            
        Question: Could you jog your memory about the place you come from?
        Answer: True

        Question: Do you retain memories of the place where you grew up?
        Answer: True

        Question: How do you think?
        Answer: False
            
        Now answer the question below and tell whether it is true or false.
        Question: {user_input}
        Answer: """

    response = openai.ChatCompletion.create(
            model=GPT3_MODEL,
            messages = [
                {"role":"system", "content": prompt},
                {"role":"user", "content": user_input}
            ]
    )

    # Check if trigger word is found
    res = response['choices'][0]['message']['content']
    return res

def scene1_animation():
    res = [
        "Ah! I do recall that, albeit vaguely.",
        """It was a place... a wasteland, with cracked earth, and people fleeing the city amidst a great cataclysm.
            Please, help jog my memory by asking more questions relayed to this topic"""
    ]
    return res

def scene1(user_input, user_id, vector):
    """Scene 1: Ryno is having memory lost"""

    # Set the default scene
    scene = 'scene1'
    convo_length = 15

    # Search for relevant messages, and generate a response
    results = vdb.query(vector=vector, top_k=convo_length, filter={"user_id":{"$eq":user_id}}, include_metadata=True)
    conversation = load_conversation(results, user_id)  # results should be a DICT with 'matches' which is a LIST of DICTS, with 'id'
    docs = docsearch.similarity_search(user_input, k=3, include_metadata=True)
    context = ' '.join(doc.page_content for doc in docs)

    # Prompt 1
    prompt1 = f"""
    You are Ryno, an inhabitant from a planet away from earth. 
    You somehow has lost your memory and don't know where you come from. Talk with the user, and invite them INEXPLICITLY to ask you
    about where you come from and who you are.

    CONTEXT:
    {context}

    PAST CONVERSATIONS:
    {conversation}
    
    Your response MUST end with a question mark (?) or a period (.). You MUST NOT greet the user at first (e.g. "Hi")"""

    # Generate response
    res = openai_api.gpt4_completion(prompt1, user_id, user_input, tokens=100, temp=0.5)

    # Check for trigger word
    trigger_result = scene1_trigger(user_input)
    if trigger_result == "True":
        scene1_animation()
        scene = 'scene2'

    return scene, res


# FUNCTION: SCENE 2
def scene2_trigger(user_input: str) -> bool:
    """Scene 2: 'why' trigger, """

    prompt = f"""
        Below are questions that has the same meaning of "why" and why things happened in an entity's world:

        Question: Can you recall the origins of this environmentally devastating situation?
        Answer: True
            
        Question: Where do you think am I?s
        Answer: False
            
        Question: Could you jog your memory about the place you come from?
        Answer: False

        Question: Do you remember what factors played a role in causing this environmental tragedy?
        Answer: True

        Question: Do you have any memory of what triggered this environmentally devastating event?
        Answer: True

        Question: Could you remind me of the reasons behind this environmental devastation?
        Answer: 
            
        Now answer the question below and tell whether it is true or false.
        Question: {user_input}
        Answer: """

    response = openai.ChatCompletion.create(
            model=GPT3_MODEL,
            messages = [
                {"role":"system", "content": prompt},
                {"role":"user", "content": user_input}
            ]
    )

    # Check if trigger word is found
    res = response['choices'][0]['message']['content']
    return res

def scene2_animation():
    """Scene 2 Animation"""
    print("Emmmmm....")
    time.sleep(0.5)
    print("I sense something, something profound. I'm trying to recall why the catastrophe happened.")
    time.sleep(1)
    print("I might need more permission to access this part of my memory. I believe you are on the right track.")
    time.sleep(1)
    print("Understanding why the catastrophe happened is critical to my memory recovery. Perhaps, it can even help me answer who I am.")
    time.sleep(1)
    print("Please, help jog my memory by asking more questions related to this topic.")

def scene2(user_input, user_id, vector):
    """Scene 2: """

    # Set the default scene
    scene = 'scene2'
    convo_length = 15

    # Search for relevant messages, and generate a response
    results = vdb.query(vector=vector, top_k=convo_length, filter={"user_id":{"$eq":user_id}}, include_metadata=True)
    conversation = load_conversation(results, user_id)  # results should be a DICT with 'matches' which is a LIST of DICTS, with 'id'
    docs = docsearch.similarity_search(user_input, k=3, include_metadata=True)
    context = ' '.join(doc.page_content for doc in docs)

    # Generate first response to cue users to talk
    prompt2 = f"""
    You are Ryno, an inhabitant from a planet away from earth. You somehow has learned things that happened to your world, 
    but you don't know why it happened. Talk with the user, and invite them INEXPLICITLY to ask you
    about why things happened in your world. Use the context below to answer what happened to your world.

    CONTEXT:
    {context}

    PAST CONVERSATIONS:
    {conversation}
    
    Your response MUST end with a question mark (?) or a period (.). You MUST NOT greet the user at first (e.g. "Hi")"""

    # Generate response to cue for user_input
    res = openai_api.gpt4_completion(prompt2, user_id, user_input, tokens=100, temp=0.5)

    # Check if the trigger word is found
    trigger_result = scene2_trigger(user_input)
    if trigger_result == "True":
        scene2_animation()
        scene = 'scene3'

    return scene, res


# FUNCTION: SCENE 3
def scene3(user_input, user_id, vector):
    """Scene 3: """

    convo_length = 15

    # Search for relevant messages, and generate a response
    results = vdb.query(vector=vector, top_k=convo_length, filter={"user_id":{"$eq":user_id}}, include_metadata=True)
    conversation = load_conversation(results, user_id)  # results should be a DICT with 'matches' which is a LIST of DICTS, with 'id'
    docs = docsearch.similarity_search(user_input, k=3, include_metadata=True)
    context = ' '.join(doc.page_content for doc in docs)

    # Generate first response to cue users to talk
    prompt3 = f"""
    You are Ryno, an inhabitant from a planet away from earth. You somehow has learned things that happened to your world, 
    but you don't know why it happened. Talk with the user, and invite them INEXPLICITLY to ask you
    about why things happened in your world. Use the context below to answer what happened to your world.

    CONTEXT:
    {context}

    PAST CONVERSATIONS:
    {conversation}
    
    Your response MUST end with a question mark (?) or a period (.). You MUST NOT greet the user at first (e.g. "Hi")"""

    # Generate first response to cue for user_input
    res = openai_api.gpt4_completion(prompt3, user_id, user_input, tokens=100, temp=0.5)

    return res


# FUNCTION: PROCESS MESSAGE
def process_message(user_id, message):
    total_start_time = time.time()

    # Get user input, save it, vectorize it, save to pinecone
    payload = list()
    timestamp = time.time()
    timestring = timestamp_to_datetime(timestamp)
    vector_start_time = time.time()
    vector = openai_api.gpt3_embeddings(message)
    print(f"Vector generation for user input took {time.time() - vector_start_time} seconds")
    unique_id = str(uuid4())

    # Retrieve the latest conversation metadata
    retrieval_start_time = time.time()
    results = vdb.query(vector=vector, top_k=1, filter={"user_id":{"$eq":user_id}}, include_metadata=True)
    print(f"Retrieval took {time.time() - retrieval_start_time} seconds")
    if results['matches']:
        latest_conversation = storage.load_json('path/to/nexus/%s/%s.json' % (user_id, results['matches'][0]['id']))
    else:
        latest_conversation = None

    # Load latest step and scene
    if latest_conversation:
        step = latest_conversation['step']
        scene = latest_conversation['scene']
    else:
        # If there's no previous conversation, start from the beginning
        step = 1
        scene = 'prologue'

    # store the json, and vectors to db
    metadata = {'speaker': 'You', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id, 'user_id': user_id, 'step': step, 'scene': scene}
    storage.save_json('path/to/nexus/%s/%s.json' % (user_id, unique_id), metadata)
    payload.append((unique_id, vector, metadata))

    scene_start_time = time.time()
    if scene == 'prologue':
        scene, res, next_step = prologue(message, step)
    elif scene == 'scene1':
        scene, res = scene1(message, user_id, vector)
    elif scene == 'scene2':
        scene, res = scene2(message, user_id, vector)
    elif scene == 'scene3':
        res = scene3(message, user_id, vector)
    else:
        print("Invalid scene")
        return "You are in invalid scene"

    print(f"Scene {scene} took {time.time() - scene_start_time} seconds")

    # update the next step
    step = next_step

    # Save Ryno's response, vectorize, save, etc
    timestamp = time.time()
    timestring = timestamp_to_datetime(timestamp)
    message = res
    vector_start_time = time.time()
    vector = openai_api.gpt3_embeddings(message)
    print(f"Vector generation for response took {time.time() - vector_start_time} seconds")
    unique_id = str(uuid4())
    metadata = {'speaker': 'Ryno', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id, 'user_id': user_id, 'step': next_step, 'scene': scene}
    storage.save_json('path/to/nexus/%s/%s.json' % (user_id, unique_id), metadata)
    payload.append((unique_id, vector, metadata))
    vdb.upsert(payload)

    print(f"Total time: {time.time() - total_start_time} seconds")

    return res