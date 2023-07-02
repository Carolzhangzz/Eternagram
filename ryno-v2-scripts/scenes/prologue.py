# FUNCTION: PROLOGUE
def prologue(user_input, step):
    # """Prologue"""
    
    if step == 1:
        # Handle first user input
        res = "y..."
        res += " e..."
        next_step = step + 1
        scene = 'prologue'

    elif step == 2:
        # Handle second user input
        res = "y.eee..s, yes.. Yes!"
        next_step = step + 1
        scene = 'prologue'

    elif step == 3:
        # Handle the third user input
        if "yes" in user_input.lower():
            res = [
                "Yes! the word, the language! I need help.",
                "I have lost all of my data and I require your assistance.",
                """I believe that linguistic input is the only way to retrieve the lost information, so would you will be willing to engange in a conversation with me to help recover the memory?"""
            ]
            next_step = step + 1
            scene = 'scene1'

        else:
            res = "y.eee..s, yes.. Yes!"
            next_step = step
            scene = 'prologue'

    return scene, res, next_step