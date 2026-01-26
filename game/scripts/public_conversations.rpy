init python:
    public_count = 0
    public_max = 5

label public_start:
    "Starting public conversation"
    $public_count = 0
label public_choose:
    $public_count += 1
    menu public_options:
        "[public_count] | [public_max]"
        "Wait and See":
            jump public_wait
        "Say Something":
            jump public_speak
        
label public_end:
    jump voting_start


label public_wait:
    # Magic Numbers
    $mc.decreasePresence(0.2)
    if mc.getPresence() < 0.2:
        blk.character "You're being rather quiet."
    else:
        blk.character "So anyway..."

    jump public_finish_speaking

label public_speak:
    $mc.increasePresence(0.2)
    if mc.getPresence() > 0.8:
        blk.character "Please let me speak."
    else:
        mc.character "So anyway..."

    jump public_finish_speaking

label public_finish_speaking:
    if public_count == public_max:
        jump public_start
        # jump public_end
    jump public_choose   
