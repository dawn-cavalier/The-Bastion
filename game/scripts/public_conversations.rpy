init python:
    public_count = 0
    public_max = 5

label public_start:
    "Starting public conversation"
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
    if public_count == public_max:
        jump public_end
    jump public_choose   

label public_speak:
    if public_count == public_max:
        jump public_end
    jump public_choose   
