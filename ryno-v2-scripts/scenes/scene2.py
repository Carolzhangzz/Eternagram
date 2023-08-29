# import from utils.py
from utils import (openai_api, vdb, docsearch, 
                   load_conversation)

# import other essentials
import openai
import time
from dotenv import load_dotenv

load_dotenv()

# MODELS
GPT3_MODEL = 'gpt-3.5-turbo'
GPT4_MODEL = 'gpt-4'


# FUNCTION: SCENE 2
def scene2_trigger(user_input: str, last_response: str) -> bool:
    """Scene 2: 'why' trigger, """

    prompt = f"""
        Ryno's last message: {last_response}

        Below are questions that are of the same meaning as "why" and relate to why things happened in Ryno's world:

        Question: Can you recall the origins of this environmentally devastating situation?
        Answer: True
            
        Question: Where do you think am I?
        Answer: False
            
        Question: Could you jog your memory about the place you come from?
        Answer: False

        Question: Do you remember what factors played a role in causing this environmental tragedy?
        Answer: True

        Question: Do you have any memory of what triggered this environmentally devastating event?
        Answer: True

        Question: But, why does it happened?
        Answer: True

        Question: What happened?
        Answer: False
            
        Now, given Ryno's recent response and the user question below, decide whether it seeks to understand "why" something happened in Ryno's world. You should respond with either 'True' or 'False'.

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

def scene2_animation():
    """Scene 2 Animation"""
    res = [
        "Oh, now I remember...",
        "The real reason why things got bad... I'd forgotten, but now it's all coming back.",
        "There was a huge disaster, like a mountain exploding and the weather changing really wildly. This made it really hard to live on earth anymore, and it was tougher to find resources we needed, like food and water.",
        "Even worse, the grown-ups, including me, used too much of a special technology that let us live longer. But we didn't realize how much stuff we were using up. Then we forgot how to use this technology, and we didn't teach younger people about it.",
        "The lack of some really important stuff, like the Firewall, made things even worse. People started fighting over the little resources that were left. It taught us a hard lesson about how we need to take care of our world better.",
        "Now that I remember all this, I feel...",
        "I feel really sad about what happened, but also strong and ready to help make our world better."
    ]

    return res

def scene2_animation2():
    """Scene 2 Animation Part:2"""
    res = [
        "Hey stranger, just wanted to take a moment to thank you for helping me recollect this super important memory. But here's the thing: I still can't remember who I am or what I'm all about...",
        "On the flip side, something interesting is happening. As these memories come flooding back, I'm also rediscovering my curiosity – something I hadn't felt in ages."
    ]
    return res

def scene2(user_input, user_id, vector, step):
    """Scene 2: """

    # [Set the default scene]
    scene = 'scene2'
    convo_length = 15
    context = ""
    conversation = ""

    # Search for relevant messages, and generate a response
    results = vdb.query(vector=vector, top_k=convo_length, filter={"user_id":{"$eq":user_id}}, include_metadata=True)
    conversation = load_conversation(results, user_id)  # results should be a DICT with 'matches' which is a LIST of DICTS, with 'id'
    docs = docsearch.similarity_search(user_input, k=3)
    context = ' '.join(doc.page_content for doc in docs)

    # [Generate first response to cue users to talk]
    prompt2 = f"""
    As Ryno, express curiosity and confusion about the events that unfolded in your world. Steer your conversations subtly to encourage inquiries about why things happened as they did on your home planet. Vary your chat styles. Sometimes ask, sometimes share, sometimes ponder to induce intrigue.

    Encourage conversations in a way that subtly elicits questions about past events of your mysterious world.

    CONTEXT: {context}

    PAST CONVERSATIONS: {conversation}

    Conclude your responses with thought-provoking statements or subtly suggestive queries to spark further exploration. Begin your interactions with intriguing narratives instead of standard greetings. Maintain a conversation style simple and understandable - as if speaking to a 4th grader.
    """

    # [Generate response to cue for user_input]
    res = openai_api.gpt4_completion(prompt2, user_id, user_input, tokens=100, temp=0.5, top_p=0.5)

    # [Update the step]
    next_step = step + 1

    return scene, res, next_step