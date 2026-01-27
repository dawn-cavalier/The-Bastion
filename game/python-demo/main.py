from random import shuffle, sample

from player_class import Player
from enums.roles import Role
from enums.characters import Character

def main() -> None:
    # Macro Game Setup
    # Create player objects
    allPlayers = [Player(character) for character in Character]

    # Micro Game Setup
    # Clear previous game
    for player in allPlayers:
        player.reset()

    # Get characters who are playing the game
    activeCharacters = [character for character in allPlayers]

    # Assign Seats
    seats = sample([seat for seat in range(len(activeCharacters))], len(activeCharacters))
    for index, seat in enumerate(seats):
        activeCharacters[index].seat = seat

    # Fill Bag
    townsfolkCount = 7
    outsiderCount = 0
    minionCount = 2
    demonCount = 1

    activeRoles = [role for role in Role]
    setupModifyingRoles = [Role.BARON]
    
    minions = sample([role for role in activeRoles if role >= Role.POISONER and role <= Role.SCARLET_WOMAN], minionCount)

    activeSetupModifyingRoles = set(minions) & set(setupModifyingRoles)

    if len(activeSetupModifyingRoles) > 0:
        if (Role.BARON in activeSetupModifyingRoles):
            outsiderCount += 2
            townsfolkCount -= 2


    townsfolk = sample([role for role in activeRoles if role >= Role.WASHERWOMAN and role <= Role.MAYOR], townsfolkCount)
    outsiders = sample([role for role in activeRoles if role >= Role.BUTLER and role <= Role.DRUNK], outsiderCount)
    demons = sample([role for role in activeRoles if role >= Role.IMP and role <= Role.IMP], demonCount)

    roleBag: list[Role] = townsfolk + outsiders + minions + demons

    # Assign Roles
    shuffle(roleBag)
    for index, role in enumerate(roleBag):
        activeCharacters[index].role = role

    for character in activeCharacters:
        print(f"{character}\n")    

if __name__ == "__main__":
    main()