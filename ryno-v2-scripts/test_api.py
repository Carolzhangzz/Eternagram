import requests

url = "http://127.0.0.1:8000/chat"  # Replace with your API endpoint URL

data = {
    "user_id": "user123",
    "message": "Hello, chatbot!"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("API response:", response.json()["response"])
else:
    print("Error:", response.status_code, response.text)

