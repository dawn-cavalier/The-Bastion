init python:
    public_count = 0
    public_max = 5

label public_start:
    "Starting public conversation"
    $public_count = 0
label public_choose:
    "[public_count] | [public_max]"
    python:
        choice: str = renpy.input("What would you like to do?", length=32)
        choice = choice.lower().strip()


    $public_count += 1

    jump public_finish_speaking  

label public_finish_speaking:
    if public_count == public_max:
        jump public_start
        # jump public_end
    jump public_choose   

label public_end:
    jump voting_start
