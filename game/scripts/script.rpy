init 2 python:
    pov = Player(0, Character("[povname]", who_color="#008080"))
    emp = Player(1, Character("Empath", who_color="#ff00a2"))
    mnk = Player(2, Character("Monk", who_color="#2fff00"))
    udr = Player(3, Character("Undertaker", who_color="#0008ff"))
    rec = Player(4, Character("Recluse", who_color="#000000"))
    imp = Player(5, Character("Imp", who_color="#FF0000"))


# The game starts here.
label start:
    scene bg room
    "Let's start"
    python:
        povname = renpy.input("What is your name?", length=32)
        povname = povname.strip()

    # pov.character "Hello!"

    # jump public_start

    # These display lines of dialogue.
    # This ends the game.
label game_exit:
    return

