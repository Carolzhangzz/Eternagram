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

    else:
        # Handle the third user input
        res = [
            "Yes! the word, the language! I need help.",
            "I've lost all of my memories and I need your help to get them back.",
            """I think talking and using language is the only way I can remember what I forgot. Would you chat with me so I can get my memory back?"""
        ]
        next_step = step + 1
        scene = 'scene1'

    return scene, res, next_step