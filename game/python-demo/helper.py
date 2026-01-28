from random import shuffle, sample

from player_class import Player
from enums.roles import Role, Alignment, Status

def buildGame(allPlayers: list[Player]) -> list[Player]:
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

    return activeCharacters

def assignRoles(characters: list[Player]) -> None:
    # TODO: Dynamic assignment
    # Fill Bag
    townsfolkCount = 7
    outsiderCount = 0
    minionCount = 2
    demonCount = 1

    # TODO: Assumes all roles active
    activeRoles = [role for role in Role]

    # TODO: More intelligently select roles
    townsfolk = sample(
        [
            role
            for role in activeRoles
            if role >= Role.WASHERWOMAN and role <= Role.MAYOR
        ],
        townsfolkCount,
    )
    outsiders = sample(
        [role for role in activeRoles if role >= Role.BUTLER and role <= Role.DRUNK],
        outsiderCount,
    )
    minions = sample(
        [
            role
            for role in activeRoles
            if role >= Role.POISONER and role <= Role.SCARLET_WOMAN
        ],
        minionCount,
    )
    demons = sample(
        [role for role in activeRoles if role >= Role.IMP and role <= Role.IMP],
        demonCount,
    )

    setupModifyingRoles = [Role.BARON]
    activeSetupModifyingRoles = set(minions) & set(setupModifyingRoles)

    if len(activeSetupModifyingRoles) > 0:
        if Role.BARON in activeSetupModifyingRoles:
            townsfolk.pop()
            townsfolk.pop()
            outsiders += sample(
                [
                    role
                    for role in activeRoles
                    if role >= Role.BUTLER
                    and role <= Role.DRUNK
                    and role not in outsiders
                ],
                2,
            )

    roleBag: list[Role] = townsfolk + outsiders + minions + demons

    # Assign Roles
    shuffle(roleBag)
    for index, role in enumerate(roleBag):
        characters[index].role = role
        if role in (townsfolk + outsiders):
            characters[index].alignment = Alignment.GOOD
        else:
            characters[index].alignment = Alignment.EVIL

    # Assign Reminder Tokens
    for character in characters:
        if character.role == Role.DRUNK:
            knownRole = sample(
                [
                    role
                    for role in activeRoles
                    if role >= Role.WASHERWOMAN
                    and role <= Role.MAYOR
                    and role not in townsfolk
                ],
                1,
            )[0]
            character.role = knownRole
            character.reminderTokens.append((Role.DRUNK, Status.IS_DRUNK))
        if character.role == Role.FORTUNE_TELLER:
            # TODO: Smarter Red Herring Logic
            redHerring = sample([character for character in characters if character.alignment == Alignment.GOOD], 1)[0]
            redHerring.reminderTokens.append((Role.FORTUNE_TELLER, Status.IS_RED_HERRING))


    # Sort by Seat Number
    characters.sort(key=lambda character: character.seat)
