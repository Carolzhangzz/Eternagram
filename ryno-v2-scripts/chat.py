import os
import json
from numpy.linalg import norm
import re
import pdfplumber
from io import BytesIO

# Google Cloud Storage Libraries
from google.cloud import storage as google_storage
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from google.auth import default

# LangChain library
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma, Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

# import from utils.py
from utils import CloudStorage, OpenAI, Page
from utils import storage, prompt_response_template, openai_api
from utils import vdb, embeddings, index_name

import openai
from dotenv import load_dotenv

from time import time,sleep
from uuid import uuid4
import datetime

connected_clients = set()

load_dotenv()

# MODELS
GPT3_MODEL = 'gpt-3.5-turbo'
GPT4_MODEL = 'gpt-4'

# Load PDF data
file_name = "Climate Change Game.pdf"
pdf_data = storage.open_binary_file(file_name)
with pdfplumber.open(BytesIO(pdf_data)) as pdf:
    # Extract text from each page and create Page objects
    data = [Page(page.extract_text()) for page in pdf.pages]

# Chunk data into smaller documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=20, separators=['\n\n', '\n', ' ', ''])
texts = text_splitter.split_documents(data)

# Passing the documents into Pinecone
docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

# Convert timestamp to datetime
def timestamp_to_datetime(unix_time):
    return datetime.datetime.fromtimestamp(unix_time).strftime("%A, %B %d, %Y at %I:%M%p %Z")

# FUNCTION: trim cut-off responses
def trim_response(response_text):
    trimmed_response = response_text.strip()
    last_period = trimmed_response.rfind(".")
    last_question = trimmed_response.rfind("?")
    last_exclamation = trimmed_response.rfind("!")
    last_end = max(last_period, last_question, last_exclamation)

    if last_end != -1:
        return trimmed_response[: last_end + 1]
    else:
        return trimmed_response
    
# FUNCTION: get response length
def get_response_length(user_input):
    input_length = len(user_input)
    if input_length <= 20:
        return 50
    elif input_length <= 100:
        return 100
    else:
        return 150
    
# FUNCTION: Load conversation fuction
def load_conversation(results, user_id):
    result = list()
    for m in results['matches']:
        # Load JSON file with correct user_id and "user_id" key in metadata
        info = storage.load_json('path/to/nexus/%s/%s.json' % (user_id, m['id']))
        if info.get('user_id') == user_id:  # check if "user_id" key in metadata matches the requested user_id
            result.append(info)
    ordered = sorted(result, key=lambda d: d['time'], reverse=False)  # sort them all chronologically
    messages = [i['message'] for i in ordered]
    return '\n'.join(messages).strip()


# FUNCTION: PROLOGUE
def prologue(user_input, user_id, vector):
    """Prologue"""

    # Asks for first user input
    user_input = input("User: ")
    if user_input != "":
        print("Ryno: y...")
        time.sleep(1)
        print("Ryno: e...")

    # Ask for second user input
    user_input = input("User: ")
    print("y.eee..s, yes.. Yes!")

    while True:
        # Asks for third user input, until trigger word is found
        user_input = input("User: ")
        if "yes" in user_input.lower():
            print("Ryno: Yes! the word, the language! I need help.")
            break
        print("y.eee..s, yes.. Yes!")

    # Perform animation for prologuea
    print("[Unknown sender]: I have lost all of my data and I require your assistance.")
    time.sleep(0.5)
    print(f"""[Unknown sender]: I believe that linguistic input is the only way to retrieve the lost information, 
                  so would you will be willing to engange in a conversation with me to help recover the memory?""")

    return 'scene1'


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
    print("Ah! I do recall that, albeit vaguely.")
    time.sleep(0.5)
    print("""It was a place... a wasteland, with cracked earth, and people fleeing the city amidst a great cataclysm.
                  Please, help jog my memory by asking more questions relayed to this topic""")

def scene1(user_input, user_id, vector):
    """Scene 1: Ryno is having memory lost"""

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
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt1},
        ],
        max_tokens=100,
        temperature=0.5
    )
    res = response['choices'][0]['message']['content']

    return 'scene1', False, res


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

    # Generate first response to cue for user_input
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt2},
        ],
        max_tokens=100,
        temperature=0.5
    )
    res = response['choices'][0]['message']['content']
    print(f"Ryno: {res}")

    return 'scene2', False, res


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
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt3},
        ],
        max_tokens=100,
        temperature=0.5
    )
    res = response['choices'][0]['message']['content']
    print(f"Ryno: {res}")

    return None


# FUNCTION: PROCESS MESSAGE
async def process_message(user_id, message, websocket, get_input_callback, scene='prologue'):

    # Get user input, save it, vectorize it, save to pinecone
    payload = list()
    timestamp = time()
    timestring = timestamp_to_datetime(timestamp)
    vector = openai_api.gpt3_embeddings(message)
    unique_id = str(uuid4())
    metadata = {'speaker': 'You', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id, 'user_id': user_id}
    storage.save_json('path/to/nexus/%s/%s.json' % (user_id, unique_id), metadata)
    payload.append((unique_id, vector, metadata))

    continue_loop = True
    while scene and continue_loop:
        if scene == 'prologue':
            scene, continue_loop, res = prologue(message, user_id, vector)
        elif scene == 'scene1':
            while continue_loop:
                scene, continue_loop, res = scene1(message, user_id, vector)
                if not continue_loop:
                    trigger_result = scene1_trigger(message)
                    if trigger_result == "True":
                        scene1_animation()
                        scene = 'scene2'
                        break
                    else:
                        continue_loop = True
        elif scene == 'scene2':
            while continue_loop:
                scene, continue_loop, res = scene2(message)
                if not continue_loop:
                    trigger_result = scene2_trigger(message)
                    if trigger_result == "True":
                        scene2_animation()
                        scene = 'scene3'
                        break
                    else:
                        continue_loop = True
        elif scene == 'scene3':
            scene, continue_loop, res = scene3(message, user_id, vector)
        else:
            print("Invalid scene")
            break

        if continue_loop:
            # Get the next user input from the ReactJS website
            message = await get_input_callback(websocket)

            # Save user input, vectorize it, save to pinecone
            timestamp = time()
            timestring = timestamp_to_datetime(timestamp)
            vector = openai_api.gpt3_embeddings(message)
            unique_id = str(uuid4())
            metadata = {'speaker': 'You', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id, 'user_id': user_id}
            storage.save_json('path/to/nexus/%s/%s.json' % (user_id, unique_id), metadata)
            payload.append((unique_id, vector, metadata))
        else:
            break

    # Save Ryno's response, vectorize, save, etc
    timestamp = time()
    timestring = timestamp_to_datetime(timestamp)
    message = res
    vector = openai_api.gpt3_embeddings(message)
    unique_id = str(uuid4())
    metadata = {'speaker': 'Ryno', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id, 'user_id': user_id}
    storage.save_json('path/to/nexus/%s/%s.json' % (user_id, unique_id), metadata)
    payload.append((unique_id, vector, metadata))
    vdb.upsert(payload)



