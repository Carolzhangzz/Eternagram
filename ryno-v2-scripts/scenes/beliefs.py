# import other essentials
from dotenv import load_dotenv

load_dotenv()

# SCENE 2: BELIEF QUESTION ITEMS
def run_scene2_questions(step):
    """Give Belief Question Items"""

    questions = [
        # Each item is a dictionary that contains a question and its responses
        {
            "question": """Now that you've heard about our world, it seems pretty different, huh?""",
            "responses": ["No kidding, it's a big change for you all.",
                          "Yeah, it's kind of interesting, I won't lie.",
                          "It doesn't seem so different to me."]
        },
        {
            "question": """For all of us who live here, this new world is strange. I'm curious though, how does it make you feel?""",
            "responses": ["Yeah, I won't lie, it's kind of scary.",
                          "I do have some worries, but I'd stay calm if I were in your place.",
                          "Just taking it as it comes."]
        },
        {
            "question": """Time sure does fly. Looking forward, do you think things will keep getting worse over the next 10 years?""",
            "responses": ["It sure seems like things aren't slowing down.",
                          "Hard to tell, but I'm ready for whatever happens.",
                          "Nope, I think the earth will heal itself."]
        },
        {
            "question": """Guessing the future is tough. What do you think about the kind of world we're leaving for kids? It's a really big thought.""",
            "responses": ["Honestly, it makes me worried. We all need to do better.",
                          "It does make me a bit nervous, but I'll try not to worry too much.",
                          "Nah, they'll figure out how to handle it."]
        },
        {
            "question": """Lots of us here think things are stuck and can't change. But do you think we can still make things better?""",
            "responses": ["Absolutely, each little thing we do can help.",
                          "I'm not sure, but I'm hopeful we can change things.",
                          "I agree, it seems stuck to me too."]
        },
        {
            "question": """Considering how our choices impact everything, do you think we're helpless or can we still do things that help? It would be awesome if we could still make things better for future generations.""",
            "responses": ["Of course, I want to do something positive.",
                          "I'm not really sure, but I'll give it my best try.",
                          "Nope, it’s already too late."]
        },
        {
            "question": """Sigh... It can feel like too much. Do you ever wonder if what we do individually can really make a difference?""",
            "responses": ["Nope, I believe every small action matters!",
                          "Sometimes I doubt it, but I try not to.",
                          "Sometimes, it feels like it doesn't matter what I do."]
        },
        {
            "question": """Do you ever feel like it's pointless to try improving our situation, or do you think that our actions as a group can make a real difference?""",
            "responses": ["I believe we can make big changes if we keep trying.",
                          "Sometimes I have doubts, but I try to stay hopeful.",
                          "Sometimes, it feels like I'm just doing the same thing over and over with no change."]
        },
        {
            "question": """So, is it important to keep learning about the things happening in our world? How important do you think it is to stay updated?""",
            "responses": ["Totally. Knowing the facts is the first step to making changes.",
                          "Sometimes, but too much information can be confusing.",
                          "I mean, even if you know everything, what can you do about it?"]
        },
    ]

    # Adjust step so it starts from index 0 (Assuming step starts from 5)
    adjusted_step = step - 5

    # Is the step within our questions range? 
    if adjusted_step >= 0 and adjusted_step < len(questions):
        res = questions[adjusted_step]
    else:
        res = "That's it! Thank you."

    next_step = step + 1 

    return 'scene2_questions', res, next_step 

