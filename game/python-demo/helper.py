from random import shuffle, sample

from player_class import Player
from enums.roles import Role
from enums.characters import Character


def assignRoles(activeCharacters: list[Player]) -> None:
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
        activeCharacters[index].setTrueRole(role)
        if role != Role.DRUNK:
            activeCharacters[index].setKnownRole(role)
        else:
            knownRole = sample(
                [role for role in activeRoles if role not in townsfolk], 1
            )[0]
            activeCharacters[index].setKnownRole(knownRole)
