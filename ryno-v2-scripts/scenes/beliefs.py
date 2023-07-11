# import other essentials
from dotenv import load_dotenv

load_dotenv()

# BELIEF QUESTION ITEMS
def run_belief_questions(step):
    """Give Belief Question Items"""

    questions = [
        """Sigh… now you have learned the reason, speaking of my world…. It's hard to ignore how different this world has become, isn't it?""",
        """The rapid changes we've witnessed have truly brought about a significant transition. In light of this new reality, I'm curious, how does it make you feel? Are you worried about it?""",
        """These concerns are shared by many, and it's interesting to observe signs around us that validate these changes, don't you think?""",
        """As time goes on, the transformation becomes increasingly apparent. Looking ahead, the question arises: do you believe my surroundings will continue to undergo such rapid changes in the next decade?""",
        """Predicting the future is challenging, but contemplating the possibilities is thought-provoking. Amidst all this uncertainty, how do you feel about the world we're leaving for the younger generations?""",
        """It's indeed a weighty thought to consider. Despite the devastating environmental circumstances, do you believe that individuals living in my world can make a positive impact?""",
        """Having faith in the power of individuals is crucial. With that in mind, do you think our actions and lifestyle choices have contributed to shaping the new world we find ourselves in?""",
        """It seems evident that our actions carry consequences. Furthermore, have you considered these changes impacting our day-to-day lives negatively?""",
        """On a more encouraging note, do you still maintain the belief that if you, personally, living in our world, can make a difference and contribute to improving the world for future generations?"""
    ]

    # Adjust step so it starts from index 0 (Assuming step starts from 6 in your case)
    adjusted_step = step - 6

    # Is the step within our questions range? 
    if adjusted_step >= 0 and adjusted_step < len(questions):
        res = questions[adjusted_step]
    else:
        res = "That's it! Thank you."

    next_step = step + 1 

    return res, next_step 