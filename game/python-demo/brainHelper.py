from enums.roles import *
import random as r


def isTownsfolk(role: Role) -> bool:
    return role >= Role.WASHERWOMAN and role <= Role.MAYOR


def isOutsider(role: Role) -> bool:
    return role >= Role.BUTLER and role <= Role.DRUNK


def isMinion(role: Role) -> bool:
    return role >= Role.POISONER and role <= Role.SCARLET_WOMAN


def isDemon(role: Role) -> bool:
    return role >= Role.IMP and role <= Role.IMP


def getTypeCounts(playerCount: int) -> tuple[int, int, int, int]:
    if playerCount < 7:
        raise Exception("Too Few Players")

    townsfolkCount = 0
    outsiderCount = 0
    minionCount = 0
    demonCount = 0

    match playerCount:
        case 5:
            townsfolkCount = 3
            outsiderCount = 0
            minionCount = 1
        case 6:
            townsfolkCount = 3
            outsiderCount = 1
            minionCount = 1
        case 7:
            townsfolkCount = 5
            outsiderCount = 0
            minionCount = 1
        case 8:
            townsfolkCount = 5
            outsiderCount = 1
            minionCount = 1
        case 9:
            townsfolkCount = 5
            outsiderCount = 2
            minionCount = 1
        case 10:
            townsfolkCount = 7
            outsiderCount = 0
            minionCount = 2
        case 11:
            townsfolkCount = 7
            outsiderCount = 1
            minionCount = 2
        case 12:
            townsfolkCount = 7
            outsiderCount = 2
            minionCount = 2
        case 13:
            townsfolkCount = 9
            outsiderCount = 0
            minionCount = 3
        case 14:
            townsfolkCount = 9
            outsiderCount = 1
            minionCount = 3
        case 15:
            townsfolkCount = 9
            outsiderCount = 2
            minionCount = 3
        case _:
            raise Exception("Too Many Players")

    demonCount = 1

    # For games with 7+ players
    # townsfolkCount = 2 * int((playerCount - 7) / 3) + 5
    # outsiderCount = (playerCount - 1) % 3
    # minionCount = int((playerCount - 4) / 3)

    return (townsfolkCount, outsiderCount, minionCount, demonCount)


def getRoles(playerCount: int, inScriptRoles: list[Role]) -> tuple[list, list]:
    townsfolkCount, outsiderCount, minionCount, demonCount = getTypeCounts(playerCount)

    activeRoles: list[Role] = []
    reminderTokens: list[list[Status]] = [[] for seat in range(playerCount)]
    drunkPresent = False
    drunkRole: Role = Role.NONE

    # Add Minions
    activeRoles += r.sample(
        [role for role in inScriptRoles if isMinion(role)], minionCount
    )
    # Check for Baron
    if Role.BARON in activeRoles:
        townsfolkCount -= 2
        outsiderCount += 2

    # Add Outsiders
    activeRoles += r.sample(
        [role for role in inScriptRoles if isOutsider(role)], outsiderCount
    )
    # Check for Drunk
    if Role.DRUNK in activeRoles:
        townsfolkCount += 1
        outsiderCount -= 1
        activeRoles.remove(Role.DRUNK)
        drunkPresent = True

    # Add Townsfolk
    activeRoles += r.sample(
        [role for role in inScriptRoles if isTownsfolk(role)], townsfolkCount
    )

    # Mark the drunk player, if present
    if drunkPresent:
        drunkRole = r.sample([role for role in activeRoles if isTownsfolk(role)], 1)[0]

    # Add Demon
    activeRoles += r.sample(
        [role for role in inScriptRoles if isDemon(role)], demonCount
    )

    r.shuffle(activeRoles)

    # Add Drunk Reminder Token
    for seat, role in enumerate(activeRoles):
        if role is drunkRole:
            reminderTokens[seat] += [Status.IS_DRUNK]

    return (activeRoles, reminderTokens)
