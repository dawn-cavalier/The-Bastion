init python:
    private_count = 0
    private_max = 5

label private_start:
    "Starting private conversation"
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
    if private_count == private_max:
        jump private_end
    jump private_choose   

label private_speak:
    if private_count == private_max:
        jump private_end
    jump private_choose   
