import math as m

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

    def __init__(
        self, seat: int, role: Role, reminderTokens: list[Status], playerCount: int
    ) -> None:
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
                Knowledge(0, None, None, InfoType.INPLAY_ROLE, [scriptDemons[0]])
            )

        # Build Role Grid
        self.buildRoleGrid(inScriptRoles=inPlayRoles)

    def __str__(self) -> str:
        return f"Seat: {self.seat}\nRole: {self.role.name}\n"

    def __getKnownInPlayRoles__(self, inScriptRoles: list[Role]) -> list[Role]:
        sumOfRoles = [0.0 for role in inScriptRoles]
        for seat, roles in enumerate(self.roleGrid):
            for roleIndex, weight in enumerate(roles):
                sumOfRoles[roleIndex] += weight

        error = 0.00005
        knownRoles: list[Role] = []
        for index, role in enumerate(inScriptRoles):
            if 1.0 - sumOfRoles[index] <= error and 1.0 - sumOfRoles[index] >= -error:
                knownRoles.append(role)
        return knownRoles

    def __getKnownNotInPlayRoles__(self, inScriptRoles: list[Role]) -> list[Role]:
        sumOfRoles = [0.0 for role in inScriptRoles]
        for seat, roles in enumerate(self.roleGrid):
            for roleIndex, weight in enumerate(roles):
                sumOfRoles[roleIndex] += weight

        error = 0.00005
        knownRoles: list[Role] = []
        for index, role in enumerate(inScriptRoles):
            if sumOfRoles[index] <= error and sumOfRoles[index] >= -error:
                knownRoles.append(role)
        return knownRoles

    def __getKnownPlayers__(self, inScriptRoles: list[Role]) -> list[tuple[int, Role]]:
        knownPlayers = []
        error = 0.00005
        for seat, roles in enumerate(self.roleGrid):
            knownRole = [
                inScriptRoles[roleIndex]
                for roleIndex, roleValue in enumerate(roles)
                if 1.0 - roleValue <= error and 1.0 - roleValue >= -error
            ]
            if len(knownRole) > 0:
                # There should only be one role per person
                knownPlayers.append((seat, knownRole[0]))
        return knownPlayers

    def __fillInUnknownRoles__(
        self,
        knowledgeList: list[Knowledge],
        startingRoleCounts: tuple[int],
        inScriptRoles: list[Role],
    ):
        townsfolk = [role for role in inScriptRoles if isTownsfolk(role)]
        outsiders = [role for role in inScriptRoles if isOutsider(role)]
        minions = [role for role in inScriptRoles if isMinion(role)]
        demons = [role for role in inScriptRoles if isDemon(role)]

        knownTownsfolk: float = 0.0
        knownOutsider: float = 0.0
        knownMinion: float = 0.0
        knownDemon: float = 0.0

        startingTownsfolk, startingOutsider, startingMinion, startingDemon = (
            startingRoleCounts
        )
        playerCount = (
            startingTownsfolk + startingOutsider + startingMinion + startingDemon
        )

        for knowledge in knowledgeList:
            match knowledge.infoType:
                case InfoType.IS_ROLE:
                    for target in knowledge.targets:
                        for role in knowledge.information:
                            if isTownsfolk(role):
                                knownTownsfolk += 1 / len(knowledge.information)
                            if isOutsider(role):
                                knownOutsider += 1 / len(knowledge.information)
                            if isMinion(role):
                                knownMinion += 1 / len(knowledge.information)
                            if isDemon(role):
                                knownDemon += 1 / len(knowledge.information)

                case InfoType.IS_NOT_ROLE:
                    # for role in knowledge.information:
                    #     if isTownsfolk(role):
                    #         knownTownsfolk += 1
                    #     if isOutsider(role):
                    #         knownOutsider += 1
                    #     if isMinion(role):
                    #         knownMinion += 1
                    #     if isDemon(role):
                    #         knownDemon += 1
                    continue

        unknownTownsfolk: float = startingTownsfolk - knownTownsfolk
        unknownOutsider: float = startingOutsider - knownOutsider
        unknownMinion: float = startingMinion - knownMinion
        unknownDemon: float = startingDemon - knownDemon

        if Role.BARON in inScriptRoles:
            adjustment = 2.0 * (startingMinion / len(minions))
            unknownOutsider += adjustment
            unknownTownsfolk -= adjustment

        if Role.DRUNK in inScriptRoles:
            adjustment = startingOutsider / len(outsiders)
            if Role.BARON in inScriptRoles:
                adjustment += ((startingOutsider + 2) / len(outsiders)) * (
                    startingMinion / len(minions)
                )
            unknownOutsider -= adjustment
            unknownTownsfolk += adjustment

        unknownPlayers = playerCount - (
            knownTownsfolk + knownOutsider + knownMinion + knownDemon
        )

        unknownTownsfolk /= unknownPlayers * (len(townsfolk) - knownTownsfolk)
        unknownOutsider /= unknownPlayers * (len(outsiders) - knownOutsider)
        if (len(minions) - knownMinion) > 0.0 and unknownPlayers > 0.0:
            unknownMinion /= unknownPlayers * (len(minions) - knownMinion)
        else:
            unknownMinion = 0.0

        if (len(demons) - knownDemon) > 0.0 and unknownPlayers > 0.0:
            unknownDemon /= unknownPlayers * (len(demons) - knownDemon)
        else:
            unknownDemon = 0.0

        for seat in range(playerCount):
            for index, role in enumerate(inScriptRoles):
                if isTownsfolk(role):
                    self.roleGrid[seat][index] = unknownTownsfolk
                elif isOutsider(role):
                    self.roleGrid[seat][index] = unknownOutsider
                elif isMinion(role):
                    self.roleGrid[seat][index] = unknownMinion
                elif isDemon(role):
                    self.roleGrid[seat][index] = unknownDemon
                else:
                    raise Exception("Invalid Role Passed In!")
                
        # Zero out not in play roles
        for knowledge in knowledgeList:
            if knowledge.infoType is not InfoType.IS_NOT_ROLE:
                continue

            for seat in range(playerCount):
                for index, role in enumerate(inScriptRoles):
                    if role in knowledge.information:
                        self.roleGrid[seat][index] = 0.0



    def __learnIsRole__(
        self, knowledge: list[Knowledge], inScriptRoles: list[Role], playerCount: int
    ):
        knowledgeST = [data for data in knowledge if data.source is None]
        knowledgePlayer = [data for data in knowledge if data.source is not None]

        if len(knowledgeST) > 0:
            self.__learnSTRoleInfo__(
                knowledge=knowledgeST,
                inScriptRoles=inScriptRoles,
                playerCount=playerCount,
            )

    def __learnSTRoleInfo__(
        self, knowledge: list[Knowledge], inScriptRoles: list[Role], playerCount: int
    ):
        knownSeats: list[int] = []
        knownRoles: list[Role] = []

        for claim in knowledge:
            targets: list[int] = [
                target for target in claim.targets if target not in knownSeats
            ]
            roles: list[Role] = [
                role for role in claim.information if role not in knownRoles
            ]

            # Uhhh, space clams?
            if len(targets) == 0 or len(roles) == 0:
                # print(f"Useless info: {claim}\nTargets: {targets}\nRoles: {roles}")
                continue

            # Logical Hard Claim
            if len(targets) == 1 and len(roles) == 1:
                if targets[0] not in knownSeats:
                    knownSeats.append(targets[0])

                if roles[0] not in knownRoles:
                    knownRoles.append(roles[0])

                for index, role in enumerate(inScriptRoles):
                    self.roleGrid[targets[0]][index] = 0.0

                for seat in range(playerCount):
                    self.roleGrid[seat][roles[0]] = 0.0

                self.roleGrid[targets[0]][roles[0]] = 1.0

            if len(targets) >= 1 and len(roles) >= 1:
                for seat in range(playerCount):
                    for index, role in enumerate(inScriptRoles):
                        if seat in targets or role in roles:
                            self.roleGrid[seat][index] = 0.0

                for seat in targets:
                    for role in roles:
                        self.roleGrid[seat][role] = 1 / len(roles)
                continue

    def buildRoleGrid(self, inScriptRoles: list[Role]):
        playerCount = [
            knowledge.information
            for knowledge in self.knowledgeBank
            if knowledge.infoType is InfoType.COUNT_PLAYERS
        ][0]

        # Reset the Grid
        self.roleGrid = [[0.0 for role in inScriptRoles] for seat in range(playerCount)]

        isRoleKnowledge: list[Knowledge] = []
        isNotRoleKnowledge: list[Knowledge] = []

        playerCount: int = 0
        townsfolkCount: int = 0
        outsiderCount: int = 0
        minionCount: int = 0
        demonCount: int = 0

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
                case InfoType.IS_ROLE:
                    isRoleKnowledge.append(knowledge)
                case InfoType.IS_NOT_ROLE:
                    isNotRoleKnowledge.append(knowledge)

        playerCount = townsfolkCount + outsiderCount + minionCount + demonCount
        self.__fillInUnknownRoles__(
            knowledgeList=isRoleKnowledge + isNotRoleKnowledge,
            startingRoleCounts=(townsfolkCount, outsiderCount, minionCount, demonCount),
            inScriptRoles=inScriptRoles,
        )

        if len(isRoleKnowledge) > 0:
            self.__learnIsRole__(
                knowledge=isRoleKnowledge,
                inScriptRoles=inScriptRoles,
                playerCount=playerCount,
            )

    def learnAndRebuildGrid(
        self, inScriptRoles: list[Role], learnedInfo: list[Knowledge]
    ):
        self.knowledgeBank += learnedInfo
        self.buildRoleGrid(inScriptRoles=inScriptRoles)

    def learnMyRole(self, inScriptRoles: list[Role]) -> None:
        learnedInfo = [
            Knowledge(
                day=0,
                source=None,
                targets=[self.seat],
                infoType=InfoType.IS_ROLE,
                information=[self.role],
            ),
            Knowledge(
                day=0,
                source=None,
                targets=[],
                infoType=InfoType.INPLAY_ROLE,
                information=[self.role],
            ),
        ]

        self.learnAndRebuildGrid(inScriptRoles=inScriptRoles, learnedInfo=learnedInfo)
