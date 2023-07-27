# import other essentials
from dotenv import load_dotenv

load_dotenv()

# SCENE 2: BELIEF QUESTION ITEMS
def run_scene2_questions(step):
    """Give Belief Question Items"""

    questions = [
        # Each item is a dictionary that contains a question and its responses
        {
            "question": """Now that you've learned about our world, It's hard to ignore how different our world has become, isn't it?""",
            "responses": ["No kidding, it's a dramatic change for you guys.",
                          "Yeah, it's so-so, I'm not gonna lie.",
                          "It's nothing."]
        },
        {
            "question": """For us, the natives... it's quite a transition. I'm wondering, how does this new  reality make you feel?""",
            "responses": ["Yeah, I can't shake off the nerves, to be honest.",
                          "I do have concerns, but I'd be calm if I were in the same situation.",
                          " just taking it as it comes."]
        },
        {
            "question": """As time goes on, it's becoming quite apparent. Looking ahead, do you think our surroundings will continue to deteriorate at this rate in the next decade?""",
            "responses": ["Looks like the train's not stopping anytime soon.",
                          "Hard to say, but I'm bracing for more possibilities.",
                          "Nope, I believe the environment will find its own way out just fine."]
        },
        {
            "question": """Predicting is always hard, isn't it? How do you feel about the kind of world we're leaving for the younger generations? It's quite a heavy thought.""",
            "responses": ["Not gonna lie, if I were you, it would keep me up at night. You guys need to do better.",
                          "It's worrisome, but I will choose to be neutral.",
                          "Nah, they'll navigate their way through."]
        },
        {
            "question": """Many inhabitants on this planet believe the situation is a deadlock. But do you think we as individuals can still shift the tide?""",
            "responses": ["Definitely, every little bit helps.",
                          "I'm on the fence, but hopeful that you guys can shift things.",
                          "You people are right, it's a deadlock."]
        },
        {
            "question": """Considering the ripple effect of our actions, do you ever wonder if we're helpless, or can we still take steps to improve our situation? It's an encouraging thought, that even amidst all this, we can do something to improve the world for future generations.""",
            "responses": ["You bet, I'm set on leaving my mark.",
                          "Not sure, but I'll give it my best shot.",
                          "No way, it’s already too late."]
        },
        {
            "question": """Sigh… It can be overwhelming, and one might wonder if individual actions really have an impact on the overall state of things. I mean, when we're talking about people versus our environment...""",
            "responses": ["No, every drop counts!",
                          "I try not to think that way, but doubt creeps in at times.",
                          "Sometimes, it feels like I'm banging my head against the wall."]
        },
        {
            "question": """But it's a good perspective to keep, acknowledging that collective efforts matter. Do you ever feel like efforts to improve the situation are futile?""",
            "responses": ["I believe we can move mountains if we keep at it.",
                          "I try not to think that way, but doubt creeps in at times.",
                          "Sometimes, it feels like I'm banging my head against the wall."]
        },
        {
            "question": """So, do you think it's important to stay informed about the issues affecting our world? We should all have the right to know, after all. How important do you think it is to stay clued up on what's happening around us?""",
            "responses": ["Very. It is essential to drive change.",
                          "Maybe, but it can also be overwhelming.",
                          "Come on, even if you know everything, what can you do?"]
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

# SCENE 3: BELIEF QUESTION ITEMS
def run_scene3_questions():
    """Give Belief Question Items"""

    questions = [
        """Now that you've learned about our world, It's hard to ignore how different our world has become, isn't it?""",
        """For us, the natives... it's quite a transition. I'm wondering, how does this new  reality make you feel?""",
        """These concerns are shared by many, and it's interesting to observe signs around us that validate these changes, don't you think?""",
        """As time goes on, the transformation becomes increasingly apparent. Looking ahead, the question arises: do you believe my surroundings will continue to undergo such rapid changes in the next decade?""",
        """Predicting the future is challenging, but contemplating the possibilities is thought-provoking. Amidst all this uncertainty, how do you feel about the world we're leaving for the younger generations?""",
        """It's indeed a weighty thought to consider. Despite the devastating environmental circumstances, do you believe that individuals living in my world can make a positive impact?""",
        """Having faith in the power of individuals is crucial. With that in mind, do you think our actions and lifestyle choices have contributed to shaping the new world we find ourselves in?""",
        """It seems evident that our actions carry consequences. Furthermore, have you considered these changes impacting our day-to-day lives negatively?""",
        """On a more encouraging note, do you still maintain the belief that if you, personally, living in our world, can make a difference and contribute to improving the world for future generations?"""
    ]
