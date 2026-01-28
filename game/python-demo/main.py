from random import shuffle, sample

from player_class import Player
from enums.roles import Role
from enums.characters import Character
from helper import assignRoles


def main() -> None:
    ## Macro Game Setup
    # Create player objects
    allPlayers = [Player(character) for character in Character]

    ## Micro Game Setup
    # Clear previous game
    for player in allPlayers:
        player.reset()

    # Get characters who are playing the game
    # TODO: Assumes all players are active players
    activeCharacters = [character for character in allPlayers]

    # Assign Seats
    seats = sample(
        [seat for seat in range(len(activeCharacters))], len(activeCharacters)
    )
    for index, seat in enumerate(seats):
        activeCharacters[index].seat = seat

    assignRoles(activeCharacters)

    for character in activeCharacters:
        if (character.role == Role.DRUNK):
            print(f"{character}\n")
            for token in character.reminderTokens:
                print(f"{token}")


    ## Start Game
    


if __name__ == "__main__":
    main()
