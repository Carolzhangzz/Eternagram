import requests
import time

user_id = "dothisornot"  # Replace with your user_id

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
        try:
            res= response.json()['response']
            if isinstance(res, list):
                for message in res:
                    print(f"Ryno: {message}")
                    time.sleep(1) # for delay in between responses
            else:
                print(f"Ryno: {res}")
        except requests.exceptions.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

if __name__ == "__main__":
    # send_receive_messages("https://ryno-v2-cedo4cgxka-de.a.run.app/message")
    send_receive_messages("http://localhost:8000/message")