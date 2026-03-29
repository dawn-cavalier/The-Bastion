import random as r

from enums.roles import *
from brainHelper import *
from enums.infoType import *


class Knowledge:
    day: int
    source: int | None
    target: int | None
    infoType: InfoType
    information: any

    def __init__(
        self,
        day: int,
        source: int | None,
        target: int | None,
        infoType: InfoType,
        information: any,
    ):
        self.day = day
        self.source = source
        self.target = target
        self.infoType = infoType
        self.information = information

    def __str__(self) -> str:
        if self.infoType is InfoType.IS_ROLE:
            if self.source is None:
                return f"On day {self.day}, Seat {self.target} learned {self.infoType.name} {self.information.name} from the Storyteller."
            return f"On day {self.day}, Seat {self.target} learned {self.infoType.name} {self.information.name} from Seat {self.source}."

        return "UNHANDLED"


class Player:
    role: Role
    seat: int
    reminderTokens: list[Status]
    knowledgeBank: list[Knowledge]
    socialTrust: list[float]
    roleGrid: list[list[float]]

    def __init__(self, seat: int, role: Role, isDrunk: bool, playerCount: int) -> None:
        self.seat = seat
        self.role = role
        self.reminderTokens = []
        self.knowledgeBank = []
        if isDrunk:
            self.reminderTokens.append(Status.IS_DRUNK)

        self.socialTrust = [0.5 for _ in range(playerCount)]
        self.roleGrid = [
            [0.0 for role in Role if role >= Role.WASHERWOMAN]
            for seat in range(playerCount)
        ]

        presentTownsfolk, presentOutsider, presentMinion, presentDemon = getTypeCounts(
            playerCount
        )

        townsfolkCount = len([_ for _ in Role if isTownsfolk(_)])
        outsiderCount = len([_ for _ in Role if isOutsider(_)])
        minionCount = len([_ for _ in Role if isMinion(_)])
        demonCount = len([_ for _ in Role if isDemon(_)])

        for playerSeat in range(playerCount):
            for playerRole in [_ for _ in Role if _ >= Role.WASHERWOMAN]:
                roleChance = 0.0
                if isTownsfolk(playerRole):
                    roleChance = presentTownsfolk / townsfolkCount

                elif isOutsider(playerRole):
                    roleChance = presentOutsider / outsiderCount

                elif isMinion(playerRole):
                    roleChance = presentMinion / minionCount

                elif isDemon(playerRole):
                    roleChance = presentDemon / demonCount

                else:
                    raise Exception("Invalid Role")

                roleChance = roleChance / playerCount
                self.roleGrid[playerSeat][playerRole] = roleChance

    def __str__(self) -> str:
        return f"Seat: {self.seat}\nRole: {self.role.name}\n"


def main() -> None:
    r.seed(a=0, version=2)
    playerCount = 8
    roles, drunkRole = getRoles(playerCount)
    players = [
        Player(
            seat=seat,
            role=roles[seat],
            isDrunk=roles[seat] is drunkRole,
            playerCount=playerCount,
        )
        for seat in list(range(playerCount))
    ]

    learnStartingInfo(players)


def learnStartingInfo(players: list[Player]) -> None:
    for player in players:
        learnedInfo = Knowledge(
            day=0,
            source=None,
            target=player.seat,
            infoType=InfoType.IS_ROLE,
            information=player.role,
        )
        # print(learnedInfo)


def getRoles(playerCount: int) -> tuple[list, Role]:
    townsfolkCount, outsiderCount, minionCount, demonCount = getTypeCounts(playerCount)

    activeRoles: list[Role] = []
    allRoles = [role for role in Role if role > -1]
    drunkPresent = False
    drunkRole: Role = Role.NONE

    activeRoles += r.sample([role for role in allRoles if isMinion(role)], minionCount)
    if Role.BARON in activeRoles:
        townsfolkCount -= 2
        outsiderCount += 2

    activeRoles += r.sample(
        [role for role in allRoles if isOutsider(role)], outsiderCount
    )
    if Role.DRUNK in activeRoles:
        townsfolkCount += 1
        outsiderCount -= 1
        activeRoles.remove(Role.DRUNK)
        drunkPresent = True

    activeRoles += r.sample(
        [role for role in allRoles if isTownsfolk(role)], townsfolkCount
    )
    if drunkPresent:
        drunkRole = r.sample([role for role in activeRoles if isTownsfolk(role)], 1)[0]

    activeRoles += r.sample([role for role in allRoles if isDemon(role)], demonCount)
    r.shuffle(activeRoles)

    return (activeRoles, drunkRole)


if __name__ == "__main__":
    main()
