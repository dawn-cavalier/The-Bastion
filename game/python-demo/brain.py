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
                return f"On day {self.day}, learned Seat {self.target} {self.infoType.name} {self.information.name} from the Storyteller."
            return f"On day {self.day}, learned Seat {self.target}  {self.infoType.name} {self.information.name} from Seat {self.source}."

        if self.infoType in (
            InfoType.INPLAY_TOWNSFOLK,
            InfoType.INPLAY_OUTSIDERS,
            InfoType.INPLAY_MINIONS,
            InfoType.INPLAY_DEMONS,
        ):
            return f"On day {self.day}, learned {self.infoType.name} {self.information}"
        
        if self.infoType in (
            InfoType.COUNT_TOWNSFOLK,
            InfoType.COUNT_OUTSIDERS,
            InfoType.COUNT_MINIONS,
            InfoType.COUNT_DEMONS
        ):
            return f"On day {self.day}, learned {self.infoType.name} is {self.information}"
        return f"UNHANDLED {self.infoType.name}"


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
        inPlayRoles = [_ for _ in Role if _ >= Role.WASHERWOMAN]

        # Innate Assumptions
        presentTownsfolk, presentOutsider, presentMinion, presentDemon = getTypeCounts(
            playerCount
        )

        demonCount = len([_ for _ in inPlayRoles if isDemon(_)])

        self.knowledgeBank += [
            Knowledge(0, None, None, InfoType.COUNT_TOWNSFOLK, (presentTownsfolk)),
            Knowledge(0, None, None, InfoType.COUNT_OUTSIDERS, (presentOutsider)),
            Knowledge(0, None, None, InfoType.COUNT_MINIONS, (presentMinion)),
            Knowledge(0, None, None, InfoType.COUNT_DEMONS, (presentDemon)),
            Knowledge(0, None, None, InfoType.INPLAY_TOWNSFOLK, ()),
            Knowledge(0, None, None, InfoType.INPLAY_OUTSIDERS, ()),
            Knowledge(0, None, None, InfoType.INPLAY_MINIONS, ()),
            Knowledge(0, None, None, InfoType.INPLAY_DEMONS, ())
        ]
        if presentDemon == demonCount:
            demonInfo = [
                knowledge
                for knowledge in self.knowledgeBank
                if knowledge.infoType is InfoType.INPLAY_DEMONS
            ][0]
            demonInfo.information = (Role.IMP,)

        for knowledge in self.knowledgeBank:
            print(knowledge)

        self.roleGrid = [[0.0 for _ in inPlayRoles] for seat in range(playerCount)]

        self.__buildRoleGrid__(playerCount=playerCount, inPlayRoles=inPlayRoles)

    def __str__(self) -> str:
        return f"Seat: {self.seat}\nRole: {self.role.name}\n"

    def __buildRoleGrid__(self, playerCount: int, inPlayRoles: list[Role]) -> None:
        presentTownsfolk, presentOutsider, presentMinion, presentDemon = getTypeCounts(
            playerCount
        )

        townsfolkCount = len([_ for _ in inPlayRoles if isTownsfolk(_)])
        outsiderCount = len([_ for _ in inPlayRoles if isOutsider(_)])
        minionCount = len([_ for _ in inPlayRoles if isMinion(_)])
        demonCount = len([_ for _ in inPlayRoles if isDemon(_)])

        

        # baronChance = presentMinion / minionCount
        # for playerSeat in range(playerCount):
        #     for playerRole in [_ for _ in inPlayRoles]:
        #         roleChance = 0.0
        #         if isTownsfolk(playerRole):
        #             # No Baron, No Drunk
        #             roleChance += (
        #                 (1 - baronChance)
        #                 * (1 - (presentOutsider / outsiderCount))
        #                 * (presentTownsfolk / townsfolkCount)
        #             )
        #             # Baron, No Drunk
        #             roleChance += (
        #                 (baronChance)
        #                 * (1 - ((presentOutsider + 2) / outsiderCount))
        #                 * ((presentTownsfolk - 2) / townsfolkCount)
        #             )
        #             # Baron, Drunk
        #             roleChance += (
        #                 (baronChance)
        #                 * ((presentOutsider + 2) / outsiderCount)
        #                 * ((presentTownsfolk - 2) / townsfolkCount)
        #             )
        #             # No Baron, Drunk
        #             roleChance += (
        #                 (1 - baronChance)
        #                 * (presentOutsider / outsiderCount)
        #                 * ((presentTownsfolk) / townsfolkCount)
        #             )

        #         elif isOutsider(playerRole):
        #             # No Baron
        #             roleChance += (1 - baronChance) * (presentOutsider / outsiderCount)
        #             # Baron
        #             roleChance += (baronChance) * (
        #                 (presentOutsider + 2) / outsiderCount
        #             )

        #         elif isMinion(playerRole):
        #             roleChance += presentMinion / minionCount

        #         elif isDemon(playerRole):
        #             roleChance += presentDemon / demonCount

        #         else:
        #             raise Exception("Invalid Role")

        #         roleChance = roleChance / playerCount
        #         self.roleGrid[playerSeat][playerRole] = roleChance

    def learn(self, playerCount: int, inPlayRoles: list[Role], knowledge: Knowledge):
        presentTownsfolk, presentOutsider, presentMinion, presentDemon = getTypeCounts(
            playerCount
        )

        townsfolkCount = len([_ for _ in inPlayRoles if isTownsfolk(_)])
        outsiderCount = len([_ for _ in inPlayRoles if isOutsider(_)])
        minionCount = len([_ for _ in inPlayRoles if isMinion(_)])
        demonCount = len([_ for _ in inPlayRoles if isDemon(_)])

        if knowledge.infoType is InfoType.IS_ROLE:
            # Storyteller information
            if knowledge.source is None:
                pass


def main() -> None:
    r.seed(a=0, version=2)
    playerCount = 7
    inPlayRoles = [_ for _ in Role if _ >= Role.WASHERWOMAN]
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

    learnStartingInfo(playerCount=playerCount, inPlayRoles=inPlayRoles, players=players)

    # print(players[0].roleGrid[0])
    # print(players[0].roleGrid[1])
    # sum = 0.0
    # for chance in players[0].roleGrid[0]:
    #     sum += chance

    # print(sum)


def learnStartingInfo(
    playerCount: int, inPlayRoles: list[Role], players: list[Player]
) -> None:
    for player in players:
        learnedInfo = Knowledge(
            day=0,
            source=None,
            target=player.seat,
            infoType=InfoType.IS_ROLE,
            information=player.role,
        )
        player.knowledgeBank.append(learnedInfo)
        print(learnedInfo)
        player.learn(
            playerCount=playerCount, inPlayRoles=inPlayRoles, knowledge=learnedInfo
        )


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
