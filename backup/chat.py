import os
import json
import numpy as np
from numpy.linalg import norm
import re
import hashlib

# Google Cloud Storage Libraries
from google.cloud import storage
from google.oauth2.service_account import Credentials

import openai
import pinecone
from dotenv import load_dotenv

from time import time,sleep
from uuid import uuid4
import datetime

load_dotenv()

class CloudStorage:
    def __init__(self, bucket_name, project_key_file):
        self.client = storage.Client.from_service_account_json(project_key_file)
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(bucket_name)

    # Load JSON file from Google Cloud Storage
    def load_json(self, filepath):
        blob = self.bucket.blob(filepath)
        return json.loads(blob.download_as_string())

    # Save JSON file to Google Cloud Storage
    def save_json(self, filepath, payload):
        blob = self.bucket.blob(filepath)
        blob.upload_from_string(json.dumps(payload))

    # Open text file from Google Cloud Storage
    def open_file(self, filepath):
        blob = self.bucket.blob(filepath)
        return blob.download_as_string().decode()

    # Save text file to Google Cloud Storage
    def save_file(self, filepath, payload):
        blob = self.bucket.blob(filepath)
        blob.upload_from_string(payload)


class OpenAI:
    def __init__(self, api_key):
        openai.api_key = api_key

    # Setup GPT-3 embeddings
    def gpt3_embeddings(self, content, engine="text-embedding-ada-002"):
        try:
            content = content.encode(encoding="ASCII", errors="ignore").decode() # fix any UNICODE errors
            response = openai.Embedding.create(input=content, engine=engine)
            vector = response['data'][0]['embedding'] # this is a normal list
            return vector
        except Exception as e:
            print(f"Error: {e}")
            return None

    # Setup GPT-3.5 completion
    def gpt3_completion(self, prompt, user_id, model='gpt-3.5-turbo', temp=0.0, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0, stop=['You:', 'Ryno:']):
        max_retry = 5
        retry = 0
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role":"user", "content": prompt}],
                    temperature=temp,
                    max_tokens=tokens,
                    top_p=top_p,
                    frequency_penalty=freq_pen,
                    presence_penalty=pres_pen,
                    stop=stop)
                
                # edit the text
                text = response['choices'][0]['message']['content'].strip()
                text = re.sub('[\r\n]+', '\n', text)
                text = re.sub('[\t ]+', ' ', text)

                filename = '%s_gpt3.txt' % time()
                if not os.path.exists('gpt3_logs/%s' % user_id):
                    os.makedirs('gpt3_logs/%s' % user_id)
                storage.save_file('gpt3_logs/%s/%s' % (user_id, filename), prompt + '\n\n==========\n\n' + text)
                return text
            except Exception as oops:
                retry += 1
                if retry >= max_retry:
                    return "GPT-3.5 error: %s" % oops
                print('Error communicating with OpenAI:', oops)
                sleep(1)


# Convert timestamp to datetime
def timestamp_to_datetime(unix_time):
    return datetime.datetime.fromtimestamp(unix_time).strftime("%A, %B %d, %Y at %I:%M%p %Z")

# Generate user id function
def generate_user_id():
    print("Please enter your username (no spaces):")
    username = input()
    return username

# Open file function (local)
def open_file2(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

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


# Set up OpenAI API key and model
openai.api_key = os.getenv("REACT_APP_OPENAI_API_KEY")
model_engine = "text-davinci-003"

# Set up Pinecone API key and index
pinecone_api_key = os.getenv("REACT_APP_PINECONE_API_KEY")
pinecone.init(api_key= pinecone_api_key, environment="us-east1-gcp")
vdb = pinecone.Index("ryno-v2")

# Initialise objects for classes
storage = CloudStorage('ryno-v2', 'my_project_key.json')
openai_api = OpenAI(openai.api_key)

if __name__ == "__main__":
    convo_length = 30

    # Get user id
    user_id = generate_user_id()
    
    while True:
        # Get user input, save it, vectorize it, save to pinecone
        payload = list()
        a = input('\n\nYou: ')
        timestamp = time()
        timestring = timestamp_to_datetime(timestamp)
        message = a
        vector = openai_api.gpt3_embeddings(message)
        unique_id = str(uuid4())
        metadata = {'speaker': 'You', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id, 'user_id': user_id}
        storage.save_json('path/to/nexus/%s/%s.json' % (user_id, unique_id), metadata)
        payload.append((unique_id, vector, metadata))


        # Search for relevant messages, and generate a response
        results = vdb.query(vector=vector, top_k=convo_length, filter={"user_id":{"$eq":user_id}}, include_metadata=True)
        conversation = load_conversation(results, user_id)  # results should be a DICT with 'matches' which is a LIST of DICTS, with 'id'
        prompt = open_file2('prompt_response.txt').replace('<<CONVERSATION>>', conversation).replace('<<MESSAGE>>', a)


        # Generate response, vectorize, save, etc
        output = openai_api.gpt3_completion(prompt, user_id)
        timestamp = time()
        timestring = timestamp_to_datetime(timestamp)
        message = output
        vector = openai_api.gpt3_embeddings(message)
        unique_id = str(uuid4())
        metadata = {'speaker': 'Ryno', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id, 'user_id': user_id}
        storage.save_json('path/to/nexus/%s/%s.json' % (user_id, unique_id), metadata)
        payload.append((unique_id, vector, metadata))
        vdb.upsert(payload)
        print('\n\nRyno: %s' % output) 
