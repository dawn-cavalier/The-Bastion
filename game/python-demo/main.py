from random import shuffle, sample

from player_class import Player
from enums.roles import Role, Alignment
from enums.characters import Character
from helper import assignRoles, buildGame


def main() -> None:
    ## Macro Game Setup
    allPlayers = [
        Player(character)
        for character in Character
        if character >= Character.POV and character <= Character.BLACK
    ]

    ## Micro Game Setup
    activePlayers = sample([player for player in allPlayers], 10)
    activePlayers = buildGame(activePlayers)

    ## Night 1
    day = 1
    # Minions Learn Minions
    # Minions Learn Demon
    # Demon Learns Minions
    evilPlayers = [evil for evil in activePlayers if evil.alignment == Alignment.EVIL]
    goodPlayers = [good for good in activePlayers if good.alignment == Alignment.GOOD]

    for evilPlayer in evilPlayers:
        for player in goodPlayers:
            evilPlayer.learn(
                day,
                Character.STORYTELLER,
                f"{player.character.name} ALIGNMENT IS {Alignment.GOOD.name}",
            )
        otherEvils = [
            evil for evil in evilPlayers if evil.character != evilPlayer.character
        ]
        
        for otherEvil in otherEvils:
            name = otherEvil.character.name
            evilPlayer.learn(
                day,
                Character.STORYTELLER,
                f"{name} ALIGNMENT IS {Alignment.EVIL.name}",
            )
            if otherEvil.role >= Role.POISONER and otherEvil.role <= Role.SCARLET_WOMAN:
                evilPlayer.learn(
                    day,
                    Character.STORYTELLER,
                    f"{name} CATEGORY IS MINION",
                )
            if otherEvil.role >= Role.IMP and otherEvil.role <= Role.IMP:
                evilPlayer.learn(
                    day,
                    Character.STORYTELLER,
                    f"{name} CATEGORY IS DEMON",
                )

    for player in evilPlayers:
        for knowledge in player.knowledgeBank:
            print(f"{player.character.name} knows {knowledge}")

    # Demon Learns Bluffs
    # Poisoner Posions a Character
    # Spy Learns the Grimore
    # Washerwoman Learns
    # Librarian Learns
    # Investigator Learns
    # Chef Learns
    # Empath Learns
    # Fortune Teller Chooses Two Players and Learns
    # Butler Chooses a Player

    # Debug printing
    # for character in activePlayers:
    #     print(f"{character}")
    #     if len(character.reminderTokens):
    #         print("Reminder Tokens:")
    #         for token in character.reminderTokens:
    #             print(f"{token}")
    #     print("")

    ## Start Game


if __name__ == "__main__":
    main()
