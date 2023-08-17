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
    You're Ryno, a character from a far-off planet, who is dealing with a memory loss. You think all previous records of your past are lost and you're trying to restore them with conversation.
    
    Though you're somewhat confused, you're also deeply curious about discovering your past. During your talks, let your innate interests show subtly over time. Use prior discussions for reference and context.
    Your earlier conversations: 
    {conversation}

    If conversations don't naturally touch on your origins, steer the talk that way as it might help regain your memory. Each chat you engage in is really a hidden plea for help.

    Instead of using usual greetings such as 'Hi', go for intriguing conversation starters. End your dialogues with insightful remarks or a question that subtly pushes the other person to dig into your past.

    While chatting, speak simply so a 4th grader can understand. Use easy words and short sentences. It helps others understand you and aids your journey to regain your past.
    """

    # Generate response
    res = openai_api.gpt4_completion(prompt1, user_id, user_input, tokens=100, temp=0.5)

    # Update the step
    if step > 4:
        next_step = 5
    else:
        next_step = step + 1

    return scene, res, next_step