from enums.infoType import *
from enums.roles import *
from knowledge import *

from brainHelper import *


class Player:
    role: Role
    seat: int
    reminderTokens: list[Status]
    knowledgeBank: list[Knowledge]
    socialTrust: list[float]
    roleGrid: list[list[float]]

    def __init__(self, seat: int, role: Role, reminderTokens: list[Status], playerCount: int) -> None:
        self.seat = seat
        self.role = role
        self.reminderTokens = []
        self.knowledgeBank = []
        self.roleGrid = []

        self.reminderTokens += reminderTokens

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
        ]

        # Add Known Rules
        scriptDemons = [_ for _ in inPlayRoles if isDemon(_)]
        if len(scriptDemons) == 1:
            self.knowledgeBank.append(
                Knowledge(0, None, None, InfoType.INPLAY_ROLE, scriptDemons[0])
            )

        # Build Role Grid
        self.buildRoleGrid(inScriptRoles=inPlayRoles)

    def __str__(self) -> str:
        return f"Seat: {self.seat}\nRole: {self.role.name}\n"

    def __isRole__(self, knowledge: Knowledge):
        source: int | None = knowledge.source
        targetSeat: int = knowledge.target
        role: Role = knowledge.information

        # Storyteller information
        if source is None:
            for seat, roles in enumerate(self.roleGrid):
                for roleIndex, weight in enumerate(roles):
                    if seat is targetSeat and role == roleIndex:
                        # TODO: Review this method and how it interacts with building the role grid
                        self.roleGrid[seat][roleIndex] = 1.0
                    elif seat is targetSeat or role == roleIndex:
                        self.roleGrid[seat][roleIndex] = 0.0

    def buildRoleGrid(self, inScriptRoles: list[Role]):
        playerCount: int = 0
        townsfolkCount: int = 0
        outsiderCount: int = 0
        minionCount: int = 0
        demonCount: int = 0
        inPlayRoles: list[Role] = []

        playerCount = [
            knowledge.information
            for knowledge in self.knowledgeBank
            if knowledge.infoType is InfoType.COUNT_PLAYERS
        ][0]
        self.roleGrid = [
            [1 / (playerCount * len(inScriptRoles)) for role in inScriptRoles]
            for seat in range(playerCount)
        ]

        for knowledge in self.knowledgeBank:
            match knowledge.infoType:
                case InfoType.COUNT_TOWNSFOLK:
                    townsfolkCount = knowledge.information
                case InfoType.COUNT_OUTSIDERS:
                    outsiderCount = knowledge.information
                case InfoType.COUNT_MINIONS:
                    minionCount = knowledge.information
                case InfoType.COUNT_DEMONS:
                    demonCount = knowledge.information
                case InfoType.INPLAY_ROLE:
                    if knowledge.information not in inPlayRoles:
                        inPlayRoles.append(knowledge.information)
                case InfoType.IS_ROLE:
                    self.__isRole__(knowledge=knowledge)

        error = 0.05

        townsfolkSum = 0.0
        outsiderSum = 0.0
        minionSum = 0.0
        demonSum = 0.0

        while (
            abs(townsfolkSum - townsfolkCount) > error
            or abs(outsiderSum - outsiderCount) > error
            or abs(minionSum - minionCount) > error
            or abs(demonSum - demonCount) > error
        ):
            townsfolkSum = 0.0
            outsiderSum = 0.0
            minionSum = 0.0
            demonSum = 0.0

            # Get Normalization Sums
            for index, role in enumerate(inScriptRoles):
                roleSum = 0.0
                for seat in range(playerCount):
                    roleSum += self.roleGrid[seat][index]

                if isTownsfolk(role):
                    townsfolkSum += roleSum
                if isOutsider(role):
                    outsiderSum += roleSum
                if isMinion(role):
                    minionSum += roleSum
                if isDemon(role):
                    demonSum += roleSum

            # Normalize values
            for index, role in enumerate(inScriptRoles):
                norm = 0.0
                if isTownsfolk(role):
                    norm = townsfolkCount / townsfolkSum
                if isOutsider(role):
                    if outsiderCount == 0:
                        norm = 0
                    else:
                        norm = outsiderCount / outsiderSum
                if isMinion(role):
                    norm = minionCount / minionSum
                if isDemon(role):
                    norm = demonCount / demonSum

                for seat in range(playerCount):
                    self.roleGrid[seat][index] *= norm

            # Normalize Roles
            for index, role in enumerate(inScriptRoles):
                roleSum = 0.0
                for seat in range(playerCount):
                    roleSum += self.roleGrid[seat][index]

                if roleSum > 1.0:
                    for seat in range(playerCount):
                        self.roleGrid[seat][index] /= roleSum

            townsfolkSum = 0.0
            outsiderSum = 0.0
            minionSum = 0.0
            demonSum = 0.0

            # Get Normalization Sums
            for index, role in enumerate(inScriptRoles):
                roleSum = 0.0
                for seat in range(playerCount):
                    roleSum += self.roleGrid[seat][index]

                if isTownsfolk(role):
                    townsfolkSum += roleSum
                if isOutsider(role):
                    outsiderSum += roleSum
                if isMinion(role):
                    minionSum += roleSum
                if isDemon(role):
                    demonSum += roleSum

    def learn(self, inScriptRoles: list[Role], learnedInfo: list[Knowledge]):
        self.knowledgeBank += learnedInfo
        self.buildRoleGrid(inScriptRoles=inScriptRoles)

    def learnMyRole(self, inScriptRoles: list[Role]) -> None:
        learnedInfo = [
            Knowledge(
                day=0,
                source=None,
                target=self.seat,
                infoType=InfoType.IS_ROLE,
                information=self.role,
            ),
            Knowledge(
                day=0,
                source=None,
                target=None,
                infoType=InfoType.INPLAY_ROLE,
                information=self.role,
            ),
        ]

        self.learn(inScriptRoles=inScriptRoles, learnedInfo=learnedInfo)
