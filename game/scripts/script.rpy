define mc = Player(0, Character("Player_Character", who_color="#008080"))
define emp = Player(1, Character("Empath", who_color="#ff00a2"))
define mnk = Player(2, Character("Monk", who_color="#2fff00"))
define udr = Player(3, Character("Undertaker", who_color="#0008ff"))
define rec = Player(4, Character("Recluse", who_color="#000000"))
define imp = Player(5, Character("Imp", who_color="#FF0000"))

# The game starts here.
label start:

    scene bg room

    # show light_blue happy
    # lb.character "Let the games begin."
    # blk.character "Yes, let's."

    jump public_start

    # These display lines of dialogue.
    # This ends the game.
label game_exit:
    return

