# The game starts here.
label start:

    scene bg room

    # show light_blue happy
    lb "Let the games begin."

    jump private_start

    # These display lines of dialogue.
    # This ends the game.
label game_exit:
    return

