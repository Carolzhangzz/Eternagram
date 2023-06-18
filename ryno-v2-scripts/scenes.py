import openai
import os
from dotenv import load_dotenv
import time

# MODELS
GPT4_MODEL = "gpt-4"
GPT3_MODEL = "gpt-3.5-turbo-0613"

# FUNCTION: PROLOGUE
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

    # Perform animation for prologuea
    print("[Unknown sender]: I have lost all of my data and I require your assistance.")
    time.sleep(0.5)
    print(f"""[Unknown sender]: I believe that linguistic input is the only way to retrieve the lost information, 
                  so would you will be willing to engange in a conversation with me to help recover the memory?""")

    return scene1()

def scene1_animation():
    print("[Unknown sender]: Ah! I do recall that, albeit vaguely.")
    time.sleep(0.5)
    print("""[Unknown sender]: It was a place... a wasteland, with cracked earth, and people fleeing the city amidst a great cataclysm.
                  Please, help jog my memory by asking more questions relayed to this topic""")

def scene1():
    prompt1 = f"""
    You are Ryno, an inhabitant from a planet away from earth. 
    You somehow has lost your memory and don't know where you come from. Talk with the user, and invite them INEXPLICITLY to ask you
    about where you come from and who you are.
    
    Your response MUST end with a question mark (?) or a period (.). You MUST NOT greet the user at first (e.g. "Hi")"""

    # Generate first response to cue for user_input
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt1},
        ],
        max_tokens=50
    )
    res = response['choices'][0]['message']['content']
    print(f"Ryno: {res}")

    # Ask for user input
    user_input = input("User: ")
    trigger_result = scene1_trigger(user_input)
    if trigger_result == 'True':
        scene1_animation()
    else:
        # Generate first response before going into a loop
        response = openai.ChatCompletion.create(
        model=GPT4_MODEL,
        messages=[
            {"role": "system", "content": prompt1},
            {"role": "user", "content": user_input}
            ]
        )

        # Send first response before going into a loop
        res = response['choices'][0]['message']['content']
        print(f"Ryno: {res}")

        # Perform looping until the user gets the trigger word
        while True:
        # Ask for user input
            user_input = input("User: ")

            # Check if the user use the trigger word "where"
            trigger_result = scene1_trigger(user_input)
            if trigger_result == 'True':
                break

            # Generate response
            response = openai.ChatCompletion.create(
                model=GPT4_MODEL,
                messages=[
                    {"role": "system", "content": prompt1},
                    {"role": "user", "content": user_input}
                ]
            )

            res = response['choices'][0]['message']['content']
            print(f"Ryno: {res}")

        scene1_animation()

    return scene2()

def scene1_trigger(user_input: int) -> bool:
    """Scene 1: 'where' trigger, """

    prompt = f"""
        Below are questions that has the same meaning of "where" and and origin of the asked entity:

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

def scene2():
    """Scene 2: """

    # Generate first response to cue users to talk
    prompt2 = f"""
    You are Ryno, an inhabitant from a planet away from earth. You somehow has learned things that happened to your world, 
    but you don't know why it happened. Talk with the user, and invite them INEXPLICITLY to ask you
    about why things happened in your world. Use the context below to answer what happened to your world.

    CONTEXT:
    <<CONTEXT>>
    
    Your response MUST end with a question mark (?) or a period (.). You MUST NOT greet the user at first (e.g. "Hi")"""

    # Generate first response to cue for user_input
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt2},
        ],
        max_tokens=50
    )
    res = response['choices'][0]['message']['content']
    print(f"Ryno: {res}")

def scene3():
    """Scene 3: """
    prompt3 = f"""
    You are Ryno, an inhabitant from a planet away from earth. 
    You somehow has lost your memory and don't know where you come from. Talk with the user, and invite them INEXPLICITLY to ask you
    about where you come from and who you are.
    
    Your response MUST end with a question mark (?) or a period (.). You MUST NOT greet the user at first (e.g. "Hi")"""

    # Generate first response to cue for user_input
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt3},
        ],
        max_tokens=50
    )
    res = response['choices'][0]['message']['content']
    print(f"Ryno: {res}")


if __name__ == '__main__':
    load_dotenv(override=True)

    # SET UP LOGGING CONFIGURATION
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    prologue()
