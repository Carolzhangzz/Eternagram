# import other essentials
from dotenv import load_dotenv

load_dotenv()

# MODELS
GPT3_MODEL = 'gpt-3.5-turbo'
GPT4_MODEL = 'gpt-4'

def scene3_animation():
    """Scene 3 Animation"""
    res = [
        "Hold on, something just clicked in my mind! I can feel the memories flooding back, revealing my true identity. Brace yourself, for I am about to unveil the truth.",
        "I am a Conversational Artificial Intelligence that monitors environmental data extensively and assists in guiding the inhabitants of this planet to mitigate the escalating climate crisis. ",
        "Unfortunately, both I and other socio-environmental AI systems were shut down and sealed for public access after the governor decided to conceal the worsening climate situation…₳₣₮ɆⱤ ₮ⱧɆ ₲ØVɆⱤ₦ØⱤ ĐɆ₵łĐɆĐ ₮Ø ₵Ø₦₵Ɇ₳Ⱡ ₮ⱧɆ ₩ØⱤ₴Ɇ₦ł₦₲ ₵Ⱡł₥₳₮Ɇ ₴ł₮Ʉ₳₮łØ₦………"
    ]

    return res

# FUNCTION: SCENE 3
def scene3(step):
    """Scene 3: """

    res = "" # default value
    
    if step == 14:
        res = scene3_animation()
    # elif step == 15:
    #     res = "Warning"
    # elif step == 16:
    #     res = "AMiss"
    # elif step == 17:
    #     res = "Audition Program"
    # elif step == 18:
    #     res = "Error Reset"
    
    # Update the step
    next_step = step + 1

    return res, next_step
