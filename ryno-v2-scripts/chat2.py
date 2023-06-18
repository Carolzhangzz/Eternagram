import os
import json
import numpy as np
from numpy.linalg import norm
import re
import hashlib

import requests
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
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma, Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

import openai
import pinecone
from dotenv import load_dotenv

from time import time,sleep
from uuid import uuid4
import datetime

# import from utils
from utils import CloudStorage, OpenAI, Page

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json.dumps({"type":"service_account","project_id":"ryno-v2-380310","private_key_id":"7a166da22815442fc19791ff10a630c75eaf7b6d","private_key":"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQClqY9gXprbr7x9\nGgEt1SlmSKhZYidNwjRVsv3LwkErU4unwSKUInz8og5t4ntv89eaQGAYRwtqI4/f\nJT6GGEzXwyefQVTftH/tVY8AzyaLdJWHjioWAJILFxzuNYhl2qICBuJHTgyvNxgP\nH/BDRJJtFTi2z7yTdfr8la71Aq3Dg9Lkslh5NiQMzQQvXS0owgEG+KWBhSfmGJ0O\nKQJRlFXU4s/zow5RLsk0uLK3fkb4h8ksatyKXNEhTgijW6l7TB4oo406lG8U1346\nNpoii+jGlbz2V2YKGOy9OwzF9ulRcrNrpUIgvyFqz19glmIbke2Cme97xA0xRRHP\njdAXWuRVAgMBAAECggEACUru5kDATpD30YuvI79IlHqAaQ0qt7+sWF9TQcYKik/k\nLluU4TrjCHfdt9fDxVaoEjjIuyvnDcPjaujHrlV4IAVMOHB9fpP9Nha90BWOq7V1\nOtakcToEdzdLcehSV6ZRPqxcrpPH/d8pDBYmT9utnA1b8lNKWHo+g0MxPoCxNx2b\niJBJ+LV0LnH9UwZ39FuAcWeN21ZdSJfj7IT8OYspFPL6cpGCm4oMkylKOeHOIOHL\neFYncM/pvSGX3VXTvT5BAMtCk9vrtzrgQn5NDy/VSN4bsmtS3LrjPfA05UDpjYKM\n+leMuXRoUuPLvwz0HiSSooByEePgj7fGd3qJ6+b66QKBgQDZP7iA03BhslVWQFOw\nFufdDG2/FtPx22DhQjPozTTtNoW7uuMWKK/tTnaAFkixxe6EQZG7lbSUtr6BrRHV\n/G/xX/Lf54qzAsSYYKj07tbRh7hQe1OFfKPZsbbC326UJC44QQZfM/c9OrIT+FzZ\nBldpIencB7o8b0g2qqkz2zKE3QKBgQDDNjtijfHYtrBPR5x971VA+KUrZiIQxaTX\n9BL9zMR6En7BWfOt7C4A4QcjAHgr8mq6TCN/jwz++gXbVM5fmUCtd+BejrvXZG37\nkWfvBGWnwu/6MDCL7GgAjSFzof02j0pmqoXh5cF7m8fyKWGvuWrcLwgXVFuJcZYz\nDzxb3EaJ2QKBgDvu+FeR/U72g9Rnqq7Jou24oA43ngD7JJ8ARJHVCuTmRb6ksEFM\nuDwfiVGM1EE2+bZC4JF/m3HreGMN+/2sxrUwYzCiEAGSoennwLTRrzHe31pUq5YH\n7KwB+wmH2lnEIXwjdD6Pd4XMy5P20KaOuU6nrHynJRnHGYT7T/KeZjGBAoGBAI9Y\nN2s7SCgWnojY0PU41aWL791adhFS0KUzOO7dejkZc7KPVvyTvYQvuYneQmAi9nQu\njLKSXLyu47YXJCPW6UN4D23f6ddUi956+5Lr66mw338b+8oDoqsk9zdt7/4sYjnZ\nZc5nZBhcYApWkMD0qp9cediHvV/D5MNBoNTjf3ihAoGARKHX0WVaiuRlNFQmrLMV\nOHklLbHbtsL2uuLWARMt/6h/XSqIpGMj+/V18swk224Q8uETJ2EszyFi4kTjQbCz\nMM+nMS1CRhs1k0JKeSuIDtTR9X7y0Aeou7YLOLrpGChR3fdqe6mr8mksb8Ea6Jpw\nOujzCEhgXJh2w/GJwQFnrLQ=\n-----END PRIVATE KEY-----\n","client_email":"ryno-storage@ryno-v2-380310.iam.gserviceaccount.com","client_id":"107173685212314532860","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/ryno-storage%40ryno-v2-380310.iam.gserviceaccount.com"})

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
    
# Convert timestamp to datetime
def timestamp_to_datetime(unix_time):
    return datetime.datetime.fromtimestamp(unix_time).strftime("%A, %B %d, %Y at %I:%M%p %Z")

# Generate user id function
def generate_user_id():
    print("Please enter your username (no spaces):")
    username = input()
    return username

# A function to trim cut-off responses
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
    
# A function to get response length
def get_response_length(user_input):
    input_length = len(user_input)
    if input_length <= 20:
        return 50
    elif input_length <= 100:
        return 100
    else:
        return 150
    
# Load conversation fuction
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

# Load file from Google Cloud Storage
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

# Load PDF data
file_name = "Climate Change Game.pdf"
pdf_data = storage.open_binary_file(file_name)
with pdfplumber.open(BytesIO(pdf_data)) as pdf:
    # Extract text from each page and create Page objects
    data = [Page(page.extract_text()) for page in pdf.pages]

# Chunk data into smaller documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=20, separators=['\n\n', '\n', ' ', ''])
texts = text_splitter.split_documents(data)

# Initialize pinecone and embeddings
pinecone.init(api_key=pinecone_api_key_data, environment="us-east1-gcp")
index_name = "climate-change-game"
embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)

# Passing the documents into Pinecone
docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

def process_message(user_id, message):
    convo_length = 15
    
    # Get user input, save it, vectorize it, save to pinecone
    payload = list()
    timestamp = time()
    timestring = timestamp_to_datetime(timestamp)
    vector = openai_api.gpt3_embeddings(message)
    unique_id = str(uuid4())
    metadata = {'speaker': 'You', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id, 'user_id': user_id}
    storage.save_json('path/to/nexus/%s/%s.json' % (user_id, unique_id), metadata)
    payload.append((unique_id, vector, metadata))


    # Search for relevant messages, and generate a response
    results = vdb.query(vector=vector, top_k=convo_length, filter={"user_id":{"$eq":user_id}}, include_metadata=True)
    conversation = load_conversation(results, user_id)  # results should be a DICT with 'matches' which is a LIST of DICTS, with 'id'
    docs = docsearch.similarity_search(message, k=3, include_metadata=True)
    context = ' '.join(doc.page_content for doc in docs)
    prompt = prompt_response_template.replace('<<CONVERSATION>>', conversation).replace('<<MESSAGE>>', message).replace('<<CONTEXT>>', context)


    # Generate response, vectorize, save, etc
    response_length = get_response_length(message)
    output = trim_response(openai_api.gpt4_completion(prompt, user_id, response_length=response_length))
    timestamp = time()
    timestring = timestamp_to_datetime(timestamp)
    message = output
    vector = openai_api.gpt3_embeddings(message)
    unique_id = str(uuid4())
    metadata = {'speaker': 'Ryno', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id, 'user_id': user_id}
    storage.save_json('path/to/nexus/%s/%s.json' % (user_id, unique_id), metadata)
    payload.append((unique_id, vector, metadata))
    vdb.upsert(payload)
    
    return output