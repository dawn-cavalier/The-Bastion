from random import shuffle, sample

from player_class import Player
from enums.roles import Role, Alignment, Status
from enums.characters import Character
from helper import *


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
    processNight(day, activePlayers)
    day += 1
    processNight(day, activePlayers)

    # Debug printing
    for player in [player for player in activePlayers]:
        print(f"{player.character.name}: {player.role.name}")
        print("Reminder Tokens:")
        print(player.reminderTokens)
        print("Knowledge Bank:")
        print(player.knowledgeBank)
        print("")
    ## Start Game


if __name__ == "__main__":
    main()
