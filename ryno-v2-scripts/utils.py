# utils.py

import os
import json
import re
from time import time, sleep
import google.cloud.storage as google_storage
from google.oauth2 import service_account
import openai
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

# Class to store json and logs
class CloudStorage:
    def __init__(self, bucket_name, project_key_json):
        project_key = json.loads(project_key_json)
        credentials = service_account.Credentials.from_service_account_info(project_key)
        self.client = google_storage.Client(credentials=credentials)
        self.bucket = self.client.bucket(bucket_name)

    # Load prompt_response.txt from Google Cloud Storage
    def load_prompt_response(self, filepath):
        return self.open_file(filepath)

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
    
    # Open binary file from Google Cloud Storage
    def open_binary_file(self, filepath):
        blob = self.bucket.blob(filepath)
        return blob.download_as_bytes()

    # Save text file to Google Cloud Storage
    def save_file(self, filepath, payload):
        blob = self.bucket.blob(filepath)
        blob.upload_from_string(payload)

# Class to use embeddings and completions
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

    # Setup GPT-4 completion
    def gpt4_completion(self, prompt, user_id, model='gpt-3.5-turbo', temp=0.7, top_p=0.8, tokens=None, freq_pen=0.0, pres_pen=0.0, stop=['You:', 'Ryno:'], response_length=None):
        max_retry = 5
        retry = 0
        tokens = tokens or response_length
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

                filename = '%s_gpt4.txt' % time()
                if not os.path.exists('gpt4_logs/%s' % user_id):
                    os.makedirs('gpt4_logs/%s' % user_id)
                storage.save_file('gpt4_logs/%s/%s' % (user_id, filename), prompt + '\n\n==========\n\n' + text)
                return text
            except Exception as oops:
                retry += 1
                if retry >= max_retry:
                    return "GPT-4 error: %s" % oops
                print('Error communicating with OpenAI:', oops)
                sleep(1)

# Class to return page_contents of large corpus PDFs
class Page:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata if metadata is not None else {}

# FUNCTION: load file from Google Cloud Storage
def load_file_from_gcs(bucket_name, filepath):
    project_key = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    credentials = service_account.Credentials.from_service_account_info(project_key)
    client = google_storage.Client(credentials=credentials)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filepath)
    return blob.download_as_string().decode()

# Load .env file from Google Cloud Storage
env_file_content = load_file_from_gcs('ryno-v2', 'keys/.env')
env_file = {line.split('=')[0]: line.split('=')[1] for line in env_file_content.split('\n') if line}

# CloudStorage initialisation
storage = CloudStorage('ryno-v2', os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

# Load prompt_response.txt from Google Cloud Storage
prompt_response_template = storage.load_prompt_response('keys/prompt_response.txt')

# Set up OpenAI API key and model
openai.api_key = env_file['REACT_APP_OPENAI_API_KEY '].strip(" '")
openai_api = OpenAI(openai.api_key)

# Set up Pinecone API key and index
pinecone_api_key = env_file['REACT_APP_PINECONE_API_KEY '].strip(" '")
pinecone.init(api_key= pinecone_api_key, environment="us-east1-gcp")
vdb = pinecone.Index("ryno-version2")

# Set up Pinecone API for knowledge base
pinecone_api_key_data = env_file['PINECONE_API_KEY_DATA '].strip(" '")
pinecone.init(api_key=pinecone_api_key_data, environment="us-east1-gcp")
index_name = "climate-change-game"
embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)