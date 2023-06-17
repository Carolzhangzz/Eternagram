import openai
import os
from dotenv import load_dotenv
import time

# MODELS
GPT4_MODEL = "gpt-4"
GPT3_MODEL = "gpt-3.5-turbo-0613"

def prologue():
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

    return scene1()

def scene1():
    prompt = f"""
    You are Ryno, an inhabitant from a planet away from earth. 
    You somehow has lost your memory and don't know where you come from. Talk with the user, and invite them INEXPLICITLY to ask you
    about where you come from and who you are.
    
    Your response MUST end with a question mark (?) or a period (.)"""

    # Generate first response to cue for user_input
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
        ],
        max_tokens=50
    )
    res = response['choices'][0]['message']['content']
    print(f"Ryno: {res}")

    while True:
    # Ask for user input
        user_input = input("User: ")

        # Check if the user use the trigger word "where"
        if scene1_trigger(user_input):
            break

        # Generate response
        response = openai.ChatCompletion.create(
            model=GPT4_MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ]
        )

    return scene2()

def scene1_trigger(user_input: int) -> bool:
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

def scene2():
    """Scene 2: """
    print("We have reach the scene2!")

if __name__ == '__main__':
    load_dotenv(override=True)

    # SET UP LOGGING CONFIGURATION
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    prologue()
