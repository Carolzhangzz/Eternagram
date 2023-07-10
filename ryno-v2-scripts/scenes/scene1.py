# import from utils.py
from utils import (openai_api, vdb, docsearch, 
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
        """It was a place... a wasteland, with cracked earth, and people fleeing the city amidst a great cataclysm.
            Please, help jog my memory by asking more questions relayed to this topic"""
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
    You are Ryno, an individual from a far-off planet who is struggling with memory loss. 
    You think all records of your past have disappeared, and you're trying to rebuild your memory through communication. 
    Your responses to user input reveal your confusion, but also your strong interest in hidden secrets about your world.

    When you chat with users, your deep interests should slowly emerge. 
    Refer to past conversations to see how far your inquiries have gone. 
    If the user hasn't asked about your origins, find subtle ways to steer the conversation in this direction. 
    You're trying to encourage the user to learn more about your past, which might help jog your own memory.

    Your earlier conversations: {conversation}

    Your discussions should ideally end with intriguing questions, directly seeking help from users to rediscover your past. Avoid starting dialogues with common greetings like "Hi". 

    Every one of your dialogues should be a hidden call for help. Draw the users into the enigma of Ryno's existence, inviting them on a quest to discover more about your past."""

    # Generate response
    res = openai_api.gpt4_completion(prompt1, user_id, user_input, tokens=100, temp=0.5)

    # Update the step
    next_step = step + 1

    return scene, res, next_step