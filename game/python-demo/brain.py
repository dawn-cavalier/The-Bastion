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
            InfoType.COUNT_DEMONS,
            InfoType.COUNT_PLAYERS,
        ):
            return (
                f"On day {self.day}, learned {self.infoType.name} is {self.information}"
            )
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
        self.roleGrid = []

        if isDrunk:
            self.reminderTokens.append(Status.IS_DRUNK)

        self.socialTrust = [0.5 for _ in range(playerCount)]
        inPlayRoles = [_ for _ in Role if _ >= Role.WASHERWOMAN]

        # Innate Assumptions
        countTownsfolk, countOutsider, countMinion, countDemon = getTypeCounts(
            playerCount
        )
        self.knowledgeBank += [
            Knowledge(0, None, None, InfoType.COUNT_PLAYERS, (playerCount)),
            Knowledge(0, None, None, InfoType.COUNT_TOWNSFOLK, (countTownsfolk)),
            Knowledge(0, None, None, InfoType.COUNT_OUTSIDERS, (countOutsider)),
            Knowledge(0, None, None, InfoType.COUNT_MINIONS, (countMinion)),
            Knowledge(0, None, None, InfoType.COUNT_DEMONS, (countDemon)),
            Knowledge(0, None, None, InfoType.INPLAY_TOWNSFOLK, ()),
            Knowledge(0, None, None, InfoType.INPLAY_OUTSIDERS, ()),
            Knowledge(0, None, None, InfoType.INPLAY_MINIONS, ()),
            Knowledge(0, None, None, InfoType.INPLAY_DEMONS, ()),
        ]

        # Add Known Rules
        demonCount = len([_ for _ in inPlayRoles if isDemon(_)])
        if countDemon == demonCount:
            demonInfo = [
                knowledge
                for knowledge in self.knowledgeBank
                if knowledge.infoType is InfoType.INPLAY_DEMONS
            ][0]
            demonInfo.information = (Role.IMP,)

        # Build Role Grid
        self.buildRoleGrid(inPlayRoles=inPlayRoles)

    def __str__(self) -> str:
        return f"Seat: {self.seat}\nRole: {self.role.name}\n"

    def __isRole__(self, knowledge: Knowledge):
        target = knowledge.target
        information: Role = knowledge.information
        print(knowledge)
        pass

    def buildRoleGrid(self, inPlayRoles: list[Role]):
        playerCount: int = 0
        townsfolkCount: int = 0
        outsiderCount: int = 0
        minionCount: int = 0
        demonCount: int = 0
        inPlayTownsfolk: list[Role] = None
        inPlayOutsider: list[Role] = None
        inPlayMinion: list[Role] = None
        inPlayDemon: list[Role] = None

        townsfolkRoles = [role for role in inPlayRoles if isTownsfolk(role)]
        outsiderRoles = [role for role in inPlayRoles if isOutsider(role)]
        minionRoles = [role for role in inPlayRoles if isMinion(role)]
        demonRoles = [role for role in inPlayRoles if isDemon(role)]

        for knowledge in self.knowledgeBank:
            match knowledge.infoType:
                case InfoType.COUNT_PLAYERS:
                    playerCount = knowledge.information
                case InfoType.COUNT_TOWNSFOLK:
                    townsfolkCount = knowledge.information
                case InfoType.COUNT_OUTSIDERS:
                    outsiderCount = knowledge.information
                case InfoType.COUNT_MINIONS:
                    minionCount = knowledge.information
                case InfoType.COUNT_DEMONS:
                    demonCount = knowledge.information
                case InfoType.INPLAY_TOWNSFOLK:
                    inPlayTownsfolk = knowledge.information
                case InfoType.INPLAY_OUTSIDERS:
                    inPlayOutsider = knowledge.information
                case InfoType.INPLAY_MINIONS:
                    inPlayMinion = knowledge.information
                case InfoType.INPLAY_DEMONS:
                    inPlayDemon = knowledge.information
                case InfoType.IS_ROLE:
                    self.__isRole__(knowledge=knowledge)

        self.roleGrid = [[0.0 for role in inPlayRoles] for seat in range(playerCount)]
        validPlayers = [seat for seat in range(playerCount)]

        for townsfolk in townsfolkRoles:
            index = inPlayRoles.index(townsfolk)
            scalar = 0.0
            if townsfolk in inPlayTownsfolk:
                scalar += 1

            for seat in validPlayers:
                self.roleGrid[seat][index] += scalar

        for outsider in outsiderRoles:
            index = inPlayRoles.index(outsider)
            scalar = 0.0
            if outsider in inPlayOutsider:
                scalar += 1

            for seat in validPlayers:
                self.roleGrid[seat][index] += scalar

        for minion in minionRoles:
            index = inPlayRoles.index(minion)
            scalar = 0.0
            if minion in inPlayMinion:
                scalar += 1

            for seat in validPlayers:
                self.roleGrid[seat][index] += scalar

        for demon in demonRoles:
            index = inPlayRoles.index(demon)
            scalar = 0.0
            if demon in inPlayDemon:
                scalar += 1

            for seat in validPlayers:
                self.roleGrid[seat][index] += scalar

    def learn(self, inPlayRoles: list[Role], knowledge: Knowledge):
        self.buildRoleGrid(inPlayRoles=inPlayRoles)
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

    learnStartingInfo(inPlayRoles=inPlayRoles, players=players)

    # for role in inPlayRoles:
    #     sum = 0.0
    #     for seat in players[0].roleGrid:
    #         sum += seat[role]
    #         print(f"{seat[role]}")
    #     print(f"{role.name}: {sum}")

    # for knowledge in players[0].knowledgeBank:
    #     print(knowledge)


def learnStartingInfo(inPlayRoles: list[Role], players: list[Player]) -> None:
    for player in players:
        learnedInfo = Knowledge(
            day=0,
            source=None,
            target=player.seat,
            infoType=InfoType.IS_ROLE,
            information=player.role,
        )
        player.knowledgeBank.append(learnedInfo)
        player.learn(inPlayRoles=inPlayRoles, knowledge=learnedInfo)


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
