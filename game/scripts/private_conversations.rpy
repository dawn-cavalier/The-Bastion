init python:
    private_count = 0
    private_max = 5

label private_start:
    "Starting private conversation"
    $private_count = 0
    
label private_choose:
    $private_count += 1
    menu private_options:
        "[private_count] | [private_max]"
        "Wait and See":
            jump private_wait
        "Say Something":
            jump private_speak
        
label private_end:
    jump public_start


label private_wait:
    # Magic Numbers
    # $lb.decreasePresence(0.2)
    # if lb.getPresence() < 0.2:
    #     blk.character "You're being rather quiet."
    # else:
    #     blk.character "So anyway..."

    jump private_finish_speaking

label private_speak:
    # Magic Numbers
    # $lb.increasePresence(0.2)
    # if lb.getPresence() > 0.8:
    #     blk.character "Please let me speak."
    # else:
    #     lb.character "So anyway..."

    jump private_finish_speaking

    
label private_finish_speaking:
    if private_count == private_max:
        # jump private_end
        jump private_start
    jump private_choose   
