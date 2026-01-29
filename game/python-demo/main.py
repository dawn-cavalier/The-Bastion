from random import shuffle, sample

from player_class import Player
from enums.roles import Role, Alignment, Status, isDemon, isMinion, isVillager, isTownsfolk, isOutsider
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
                f"PLAYER {player.character.name} ALIGNMENT IS {Alignment.GOOD.name}",
            )
        otherEvils = [
            evil for evil in evilPlayers if evil.character != evilPlayer.character
        ]

        for otherEvil in otherEvils:
            name = otherEvil.character.name
            evilPlayer.learn(
                day,
                Character.STORYTELLER,
                f"PLAYER {name} ALIGNMENT IS {Alignment.EVIL.name}",
            )
            if isMinion(otherEvil.role):
                evilPlayer.learn(
                    day,
                    Character.STORYTELLER,
                    f"PLAYER {name} CATEGORY IS MINION",
                )
            if isDemon(otherEvil.role):
                evilPlayer.learn(
                    day,
                    Character.STORYTELLER,
                    f"PLAYER {name} CATEGORY IS DEMON",
                )

    # Demon Learns Bluffs
    demons = [
        player
        for player in activePlayers
        if isDemon(player.role)
    ]
    for demon in demons:
        inPlayTownRoles = [
            player.role
            for player in activePlayers
            if isVillager(player.role)
        ]

        notInPlayTownRoles = [
            role
            for role in Role
            if role not in inPlayTownRoles
            and isVillager(role)
            and role is not Role.DRUNK
        ]

        # TODO: Smarter Bluff Selection Logic
        bluffs = sample(notInPlayTownRoles, 3)
        for bluff in bluffs:
            demon.learn(day, Character.STORYTELLER, f"ROLE {bluff.name} IS NOT IN PLAY")

        # for x in demon.knowledgeBank:
        #     print(x)

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
    for character in activePlayers:
        print(f"{character}")
        if len(character.reminderTokens):
            print("Reminder Tokens:")
            for token in character.reminderTokens:
                print(f"{token}")
        print("")

    ## Start Game


if __name__ == "__main__":
    main()
