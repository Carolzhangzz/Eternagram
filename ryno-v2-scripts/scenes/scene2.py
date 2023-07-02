# import from utils.py
from utils import (storage, openai_api, vdb, docsearch, 
                   load_conversation, timestamp_to_datetime)

# import other essentials
import openai
from dotenv import load_dotenv

load_dotenv()

# MODELS
GPT3_MODEL = 'gpt-3.5-turbo'
GPT4_MODEL = 'gpt-4'


# FUNCTION: SCENE 2
def scene2_trigger(user_input: str) -> bool:
    """Scene 2: 'why' trigger, """

    prompt = f"""
        Below are questions that has the same meaning of "why" and why things happened in an entity's world:

        Question: Can you recall the origins of this environmentally devastating situation?
        Answer: True
            
        Question: Where do you think am I?s
        Answer: False
            
        Question: Could you jog your memory about the place you come from?
        Answer: False

        Question: Do you remember what factors played a role in causing this environmental tragedy?
        Answer: True

        Question: Do you have any memory of what triggered this environmentally devastating event?
        Answer: True

        Question: Could you remind me of the reasons behind this environmental devastation?
        Answer: 
            
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

def scene2_animation():
    """Scene 2 Animation"""
    res = [
        "Emmmmm....",
        "I sense something, something profound. I'm trying to recall why the catastrophe happened.",
        "I might need more permission to access this part of my memory. I believe you are on the right track.",
        "Understanding why the catastrophe happened is critical to my memory recovery. Perhaps, it can even help me answer who I am.",
        "Please, help jog my memory by asking more questions related to this topic."
    ]

    return res

def scene2(user_input, user_id, vector, step):
    """Scene 2: """

    # Set the default scene
    scene = 'scene2'
    convo_length = 15
    context = ""
    conversation = ""

    # if the user has talk about anything starting from scene1 -> messages stored.
    if step > 4:
        # Search for relevant messages, and generate a response
        results = vdb.query(vector=vector, top_k=convo_length, filter={"user_id":{"$eq":user_id}}, include_metadata=True)
        conversation = load_conversation(results, user_id)  # results should be a DICT with 'matches' which is a LIST of DICTS, with 'id'
        docs = docsearch.similarity_search(user_input, k=3)
        context = ' '.join(doc.page_content for doc in docs)

    # Generate first response to cue users to talk
    prompt2 = f"""
    You are Ryno, an inhabitant from a planet away from earth. You somehow has learned things that happened to your world, 
    but you don't know why it happened. Talk with the user, and invite them INEXPLICITLY to ask you
    about why things happened in your world. Use the context below to answer what happened to your world.

    CONTEXT:
    {context}

    PAST CONVERSATIONS:
    {conversation}
    
    Your response MUST end with a question mark (?) or a period (.). You MUST NOT greet the user at first (e.g. "Hi")"""

    # Generate response to cue for user_input
    res = openai_api.gpt4_completion(prompt2, user_id, user_input, tokens=100, temp=0.5)

    # Check if the trigger word is found
    trigger_result = scene2_trigger(user_input)
    if trigger_result == "True":
        scene2_animation()
        scene = 'scene3'

    # Update the step
    next_step = step + 1

    return scene, res, next_step