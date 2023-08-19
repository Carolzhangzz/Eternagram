import requests
import time

user_id = "gogo"  # Replace with your user_id
password = "12"
  
def send_receive_messages(url, password):

    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        data = {
            "user_id": user_id,
            "password": password,
            "message": user_input
        }
        print(f"Sending data: {data}")
        response = requests.post(url, json=data)
        print(f"Status code: {response.status_code}")

        try:
            response_json = response.json()

            if 'response' in response_json:
                res = response_json['response']
                if isinstance(res, list):
                    for message in res:
                        print(f"Ryno: {message}")
                        time.sleep(1) # for delay in between responses
                else:
                    if isinstance(res, str):
                        if "Invalid password. Please try again." in res:
                            print(f"Invalid password for existing user {user_id}.")
                        elif "Your user account has been created. Your password is: " in res:
                            password = res.replace("Your user account has been created. Your password is: ","")
                            print(f"New password for user {user_id}: {password}")
                        elif "Unexpected password for new user. Leave it blank on first entry." in res:
                            print(f"{res}")
                        else:
                            print(f"Ryno: {res}")
            else:
                print(f"Unexpected response: {response_json}")
        except requests.exceptions.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

if __name__ == "__main__":
    # send_receive_messages("https://ryno-v2-cedo4cgxka-de.a.run.app/message", password)
    send_receive_messages("http://localhost:8000/message", password)