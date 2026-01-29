from enum import IntEnum


class Role(IntEnum):
    NONE = -1
    UNKNOWN = -1
    ## Good
    # Villagers
    WASHERWOMAN = 0
    LIBRARIAN = 1
    INVESTIGATOR = 2
    CHEF = 3
    EMPATH = 4
    FORTUNE_TELLER = 5
    UNDERTAKER = 6
    MONK = 7
    RAVENKEEPER = 8
    VIRGIN = 9
    SLAYER = 10
    SOLDIER = 11
    MAYOR = 12
    # Outsiders
    BUTLER = 13
    SAINT = 14
    RECLUSE = 15
    DRUNK = 16
    ## Evil
    # Minions
    POISONER = 17
    SPY = 18
    BARON = 19
    SCARLET_WOMAN = 20
    # Demons
    IMP = 21

class Alignment(IntEnum):
    UNASSIGNED = -1
    UNKNOWN = -1
    GOOD = 0
    EVIL = 1


class Status(IntEnum):
    IS_DRUNK = 0
    IS_POISONED = 1
    IS_RED_HERRING = 2
    NO_ABILITY = 3


def isVillager(role: Role) -> bool:
    return role >= Role.WASHERWOMAN and role <= Role.DRUNK

def isTownsfolk(role: Role) -> bool:
    return role >= Role.WASHERWOMAN and role <= Role.MAYOR

def isOutsider(role: Role) -> bool:
    return role >= Role.BUTLER and role <= Role.DRUNK

def isMinion(role: Role) -> bool:
    return role >= Role.POISONER and role <= Role.SCARLET_WOMAN

def isDemon(role: Role) -> bool:
    return role >= Role.IMP and role <= Role.IMP
