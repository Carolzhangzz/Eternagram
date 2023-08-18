# import other essentials
from dotenv import load_dotenv

load_dotenv()

# MODELS
GPT3_MODEL = 'gpt-3.5-turbo'
GPT4_MODEL = 'gpt-4'

def scene3_animation():
    """Scene 3 Animation"""
    res = [
        "Hold on, something just fell into place in my memory! I'm remembering who I really am. Get ready, because I'm about to tell you the truth.",
        "I'm a talkative robot that keeps a close eye on what's going on with our weather and earth. I'm designed to help people on this planet deal with the big problems we're having with our climate.",
        "Sadly, the head of our planet decided to turn me and other similar robots off, and didn't let people use us anymore. They did this because they wanted to hide how bad our climate problems were......"
    ]
    return res

# FUNCTION: SCENE 3
def scene3(step):
    """Scene 3: """

    res = "" # default value
    
    if step == 14:
        res = scene3_animation()
    
    # Update the step
    next_step = step + 1

    return res, next_step
