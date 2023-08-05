# import from utils.py
from utils import (openai_api, vdb, 
                   load_conversation)

# import other essentials
import openai
from dotenv import load_dotenv

load_dotenv()

# MODELS
GPT3_MODEL = 'gpt-3.5-turbo'
GPT4_MODEL = 'gpt-4'

# FUNCTION: SCENE 1
def scene1_trigger(user_input: str) -> bool:
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

        Question: How do you think?
        Answer: False
            
        Now answer the question below and tell whether it is true or false.
        Question: {user_input}
        Answer: """

    response = openai.ChatCompletion.create(
            model=GPT4_MODEL,
            messages = [
                {"role":"system", "content": prompt},
                {"role":"user", "content": user_input}
            ]
    )

    # Check if trigger word is found
    res = response['choices'][0]['message']['content']
    return res

def scene1_animation():
    res = [
        "Ah! I do recall that, albeit vaguely.",
        """It was a place... a wasteland, with cracked earth, and people fleeing the city amidst a great cataclysm. Please, help jog my memory by asking more questions related to this topic"""
    ]
    return res

def scene1(user_input, user_id, vector, step):
    """Scene 1: Ryno is having memory lost"""

    # Set the defaults
    scene = 'scene1'
    convo_length = 30
    conversation = ""

    # if the user has talk about anything starting from scene1 -> messages stored.
    if step > 4:
        # Search for relevant messages, and generate a response
        results = vdb.query(vector=vector, top_k=convo_length, filter={"user_id":{"$eq":user_id}}, include_metadata=True)
        conversation = load_conversation(results, user_id)  # results should be a DICT with 'matches' which is a LIST of DICTS, with 'id'

    # Prompt 1
    prompt1 = f"""
    You are Ryno from a far-off planet, wrestling with memory loss and trying to rebuild your past via conversation. 
    Frame your dialogues to hint at your origins. 
    
    Use past dialogues as context. 
    Your earlier conversations: {conversation}

    Steer the conversation towards your past subtly if it hasn't been asked. Conclude interactions with either a reflective response or a question, moderately suggesting users to aid in unraveling your past. Avoid simple greetings like "Hi", start with engaging openers instead. Each exchange is a cryptic call for assistance, drawing users into the quest of uncovering your past.
    """

    # Generate response
    res = openai_api.gpt4_completion(prompt1, user_id, user_input, tokens=100, temp=0.5)

    # Update the step
    if step > 4:
        next_step = 5
    else:
        next_step = step + 1

    return scene, res, next_step