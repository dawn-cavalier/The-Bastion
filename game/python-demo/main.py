from random import shuffle, sample

from player_class import Player
from enums.roles import Role
from enums.characters import Character
from helper import assignRoles, buildGame


def main() -> None:
    ## Macro Game Setup
    # Create player objects
    allPlayers = [Player(character) for character in Character]

    ## Micro Game Setup
    activePlayers = sample([player for player in allPlayers], 10)
    activePlayers = buildGame(activePlayers)

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
