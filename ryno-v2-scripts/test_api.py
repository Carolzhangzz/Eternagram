import requests

user_id = "latisha"  # Replace with your user_id

def send_receive_messages(url):
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        data = {
            "user_id": user_id,
            "message": user_input
        }
        response = requests.post(url, json=data)
        print(f"Status code: {response.status_code}")
        print(f"Raw response: {response.text}")
        try:
            print(f"Received: {response.json()['response']}")
        except requests.exceptions.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

if __name__ == "__main__":
    # send_receive_messages("https://ryno-v2-cedo4cgxka-de.a.run.app/message")
    send_receive_messages("http://localhost:8000/message")