# utils.py

import os
import json
import re
from time import time, sleep
import google.cloud.storage as google_storage
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound

import openai
import pinecone
import datetime
import pdfplumber
from io import BytesIO

# For password 
from random import randint
from werkzeug.security import generate_password_hash, check_password_hash

# LangChain library
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json.dumps({"type":"service_account","project_id":"ryno-v2-380310","private_key_id":"7a166da22815442fc19791ff10a630c75eaf7b6d","private_key":"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQClqY9gXprbr7x9\nGgEt1SlmSKhZYidNwjRVsv3LwkErU4unwSKUInz8og5t4ntv89eaQGAYRwtqI4/f\nJT6GGEzXwyefQVTftH/tVY8AzyaLdJWHjioWAJILFxzuNYhl2qICBuJHTgyvNxgP\nH/BDRJJtFTi2z7yTdfr8la71Aq3Dg9Lkslh5NiQMzQQvXS0owgEG+KWBhSfmGJ0O\nKQJRlFXU4s/zow5RLsk0uLK3fkb4h8ksatyKXNEhTgijW6l7TB4oo406lG8U1346\nNpoii+jGlbz2V2YKGOy9OwzF9ulRcrNrpUIgvyFqz19glmIbke2Cme97xA0xRRHP\njdAXWuRVAgMBAAECggEACUru5kDATpD30YuvI79IlHqAaQ0qt7+sWF9TQcYKik/k\nLluU4TrjCHfdt9fDxVaoEjjIuyvnDcPjaujHrlV4IAVMOHB9fpP9Nha90BWOq7V1\nOtakcToEdzdLcehSV6ZRPqxcrpPH/d8pDBYmT9utnA1b8lNKWHo+g0MxPoCxNx2b\niJBJ+LV0LnH9UwZ39FuAcWeN21ZdSJfj7IT8OYspFPL6cpGCm4oMkylKOeHOIOHL\neFYncM/pvSGX3VXTvT5BAMtCk9vrtzrgQn5NDy/VSN4bsmtS3LrjPfA05UDpjYKM\n+leMuXRoUuPLvwz0HiSSooByEePgj7fGd3qJ6+b66QKBgQDZP7iA03BhslVWQFOw\nFufdDG2/FtPx22DhQjPozTTtNoW7uuMWKK/tTnaAFkixxe6EQZG7lbSUtr6BrRHV\n/G/xX/Lf54qzAsSYYKj07tbRh7hQe1OFfKPZsbbC326UJC44QQZfM/c9OrIT+FzZ\nBldpIencB7o8b0g2qqkz2zKE3QKBgQDDNjtijfHYtrBPR5x971VA+KUrZiIQxaTX\n9BL9zMR6En7BWfOt7C4A4QcjAHgr8mq6TCN/jwz++gXbVM5fmUCtd+BejrvXZG37\nkWfvBGWnwu/6MDCL7GgAjSFzof02j0pmqoXh5cF7m8fyKWGvuWrcLwgXVFuJcZYz\nDzxb3EaJ2QKBgDvu+FeR/U72g9Rnqq7Jou24oA43ngD7JJ8ARJHVCuTmRb6ksEFM\nuDwfiVGM1EE2+bZC4JF/m3HreGMN+/2sxrUwYzCiEAGSoennwLTRrzHe31pUq5YH\n7KwB+wmH2lnEIXwjdD6Pd4XMy5P20KaOuU6nrHynJRnHGYT7T/KeZjGBAoGBAI9Y\nN2s7SCgWnojY0PU41aWL791adhFS0KUzOO7dejkZc7KPVvyTvYQvuYneQmAi9nQu\njLKSXLyu47YXJCPW6UN4D23f6ddUi956+5Lr66mw338b+8oDoqsk9zdt7/4sYjnZ\nZc5nZBhcYApWkMD0qp9cediHvV/D5MNBoNTjf3ihAoGARKHX0WVaiuRlNFQmrLMV\nOHklLbHbtsL2uuLWARMt/6h/XSqIpGMj+/V18swk224Q8uETJ2EszyFi4kTjQbCz\nMM+nMS1CRhs1k0JKeSuIDtTR9X7y0Aeou7YLOLrpGChR3fdqe6mr8mksb8Ea6Jpw\nOujzCEhgXJh2w/GJwQFnrLQ=\n-----END PRIVATE KEY-----\n","client_email":"ryno-storage@ryno-v2-380310.iam.gserviceaccount.com","client_id":"107173685212314532860","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/ryno-storage%40ryno-v2-380310.iam.gserviceaccount.com"})

# Class to store json and logs
class CloudStorage:
    def __init__(self, bucket_name, project_key_json):
        project_key = json.loads(project_key_json)
        credentials = service_account.Credentials.from_service_account_info(project_key)
        self.client = google_storage.Client(credentials=credentials)
        self.bucket = self.client.bucket(bucket_name)

    # Check if file exists
    def file_exists(self, filepath):
        blob = self.bucket.blob(filepath)
        return blob.exists()
    
    # Check if the user exists
    def check_user_exits(self, user_id):
        filepath = 'users/%s/password' % user_id
        return self.file_exists(filepath)
    
    # Retrieve hashed password for a user
    def retrieve_hashed_password(self, user_id):
        filepath = 'users/%s/password' % user_id
        if self.file_exists(filepath):
            hashed_password = self.open_file(filepath) 
            return hashed_password
        else:
            return None
        
    # Save a user's id and hashed password
    def save_user(self, user_id, hashed_password):
        filepath = 'users/%s/password' % user_id
        self.save_file(filepath, hashed_password)
    
    # Load JSON file to Google Cloud Storage
    def load_json(self, filepath):
        try:
            if self.file_exists(filepath):
                blob = self.bucket.blob(filepath)
                return json.loads(blob.download_as_string())
            else:
                print(f"File {filepath} does not exist.")
                return None
        except Exception as e:
            print(f"An error occurred while loading JSON: {e}")
            return None
        
    # Save JSON file to Google Cloud Storage
    def save_json(self, filepath, payload):
        try:
            blob = self.bucket.blob(filepath)
            blob.upload_from_string(json.dumps(payload))
        except Exception as e:
            print(f"An error occurred while saving JSON: {e}")

    # Open text file from Google Cloud Storage
    def open_file(self, filepath):
        if self.file_exists(filepath):
            blob = self.bucket.blob(filepath)
            return blob.download_as_string().decode()
        else:
            print(f"File {filepath} does not exist.")
            return None
    
    # Open binary file from Google Cloud Storage
    def open_binary_file(self, filepath):
        blob = self.bucket.blob(filepath)
        return blob.download_as_bytes()

    # Save text file to Google Cloud Storage
    def save_file(self, filepath, payload):
        blob = self.bucket.blob(filepath)
        blob.upload_from_string(payload)

    # Get the latest file from GCS
    def get_latest_file(self, user_id):
        # Get the list of all blobs in the specified user_id directory
        blobs = self.bucket.list_blobs(prefix=f'path/to/nexus/{user_id}')

        # Initialize the latest_blob
        latest_blob = None

        for blob in blobs:
            # Discard any directories (as they have no 'updated' attribute)
            if not blob.name.endswith("/"):
                # Always select the first blob as the latest blob 
                if latest_blob is None:
                    latest_blob = blob
                # Select the blob with the latest 'updated' attribute
                elif blob.updated > latest_blob.updated:
                    latest_blob = blob

        # now, latest_blob is the most recent blob for the user_id
        if latest_blob is not None:
            try:
                # To get metadata (dict)
                metadata = dict(latest_blob.metadata or {})

                # To download the blob as string
                json_string = latest_blob.download_as_text()

                return metadata, json_string
            except NotFound:
                print(f"No such object: {latest_blob.name}")
                return None, None
        else:
            print(f"No files found for user: {user_id}")
            return None, None

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
    def gpt4_completion(self, prompt, user_id, message, model='gpt-4', temp=0.7, top_p=0.8, tokens=None, freq_pen=0.0, pres_pen=0.0, stop=['You:', 'Ryno:'], response_length=None):
        max_retry = 5
        retry = 0
        tokens = tokens or response_length
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role":"system", "content": prompt}, 
                        {"role":"user", "content": message}
                        ],
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

# Class for password managing
class PasswordManager:
    def __init__(self, storage):
        self.storage = storage
    
    # FUNCTION: generate password hash
    def generate_password_hash(self, password):
        return generate_password_hash(password)

    # FUNCTION: check the password
    def check_password(self, user_id, entered_password):
        hashed_pwd = self.storage.retrieve_hashed_password(user_id)

        # Check password
        is_password_correct = check_password_hash(hashed_pwd, entered_password)

        return is_password_correct

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

# Objects initialisation
storage = CloudStorage('ryno-v2', os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
password_manager = PasswordManager(storage)

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

# FUNCTION: Load last response from Ryno
def get_last_response(user_id: str, speaker: str = 'Ryno') -> str:
    """Get the latest response from the mentioned speaker if exists, else returns an empty string."""
    
    metadata, latest_conversation_json = storage.get_latest_file(user_id)

    if latest_conversation_json:
        latest_conversation = json.loads(latest_conversation_json)
        
        # Checks if the last speaker is 'Ryno'
        if latest_conversation['speaker'] == speaker:
            return latest_conversation['message']
    
    return ""