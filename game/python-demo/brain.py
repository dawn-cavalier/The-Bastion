import random as r  

from enums.roles import *

class Player:
    role: Role
    seat: int 
    isDrunk: bool
    def __init__(self, seat, role) -> None:
        self.seat = seat
        self.role = role
        self.isDrunk = False

    def __str__(self) -> str:
        return f"Seat: {self.seat}\nRole: {self.role.name}\nIs Drunk: {self.isDrunk}"
    
    def setDrunk(self, state) -> None:
        self.isDrunk = state


def isTownsfolk(role: Role) -> bool:
    return role >= Role.WASHERWOMAN and role <= Role.MAYOR
def isOutsider(role: Role) -> bool:
    return role >= Role.BUTLER and role <= Role.DRUNK
def isMinion(role: Role) -> bool:
    return role >= Role.POISONER and role <= Role.SCARLET_WOMAN
def isDemon(role: Role) -> bool:
    return role >= Role.IMP and role <= Role.IMP

def getRoles() -> tuple[list, Role]:
    # Fill Bag
    townsfolkCount = 7
    outsiderCount = 2
    minionCount = 2
    demonCount = 1

    activeRoles: list[Role] = []
    allRoles = [role for role in Role if role > -1]
    drunkPresent = False
    drunkRole: Role = Role.NONE

    activeRoles += r.sample([role for role in allRoles if isMinion(role)], minionCount)
    if Role.BARON in activeRoles:
        townsfolkCount -= 2
        outsiderCount += 2

    activeRoles += r.sample([role for role in allRoles if isOutsider(role)], outsiderCount)
    if Role.DRUNK in activeRoles:
        townsfolkCount += 1
        outsiderCount -= 1
        activeRoles.remove(Role.DRUNK)
        drunkPresent = True

    activeRoles += r.sample([role for role in allRoles if isTownsfolk(role)], townsfolkCount)
    if drunkPresent:
        drunkRole = r.sample([role for role in activeRoles if isTownsfolk(role)], 1)[0]

    activeRoles += r.sample([role for role in allRoles if isDemon(role)], demonCount)
    r.shuffle(activeRoles)

    return (activeRoles, drunkRole)

def main() -> None:
    r.seed(a=None, version=2)

    roles, drunkRole = getRoles()
    players = [Player(seat, roles[seat]) for seat in list(range(12))]
    drunkPlayers = [player for player in players if player.role is drunkRole]
    if len(drunkPlayers) > 0:
        for player in drunkPlayers:
            player.setDrunk(True)

    for player in players:
        print(player)
    return

if __name__ == "__main__":
    main()
