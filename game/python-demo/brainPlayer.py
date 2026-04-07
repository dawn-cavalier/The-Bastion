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

    def __isRole__(
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
        # Get the Hard Claims
        hardClaims = [info for info in knowledge if len(info.information) == 1]
        softClaims = [info for info in knowledge if len(info.information) != 1]

        for hardClaim in hardClaims:
            targetSeat: int = hardClaim.target
            learnedRole: Role = hardClaim.information[0]

            # Learn Hard Claims
            for seat, roles in enumerate(self.roleGrid):
                for roleIndex, weight in enumerate(roles):
                    if seat is targetSeat and roleIndex == learnedRole:
                        self.roleGrid[seat][roleIndex] = 1.0
                    elif seat is targetSeat or roleIndex == learnedRole:
                        self.roleGrid[seat][roleIndex] = 0.0

            # Reduce and recalculate the soft claims by the hard claims
            for softClaim in softClaims:
                if learnedRole in softClaim.information:
                    # TODO: THIS REMOVES THE ITEM FROM THE ORIGINAL ARRAY. THIS CAN'T WORK FOR NON-STORYTELLER INFO
                    softClaim.information.remove(learnedRole)

            for softClaim in softClaims:
                targetSeat: int = softClaim.target
                learnedRoles: tuple[Role] = softClaim.information

                for seat, roles in enumerate(self.roleGrid):
                    for roleIndex, weight in enumerate(roles):
                        if seat is targetSeat and roleIndex in learnedRoles:
                            self.roleGrid[seat][roleIndex] = 1.0 / len(learnedRoles)
                        elif seat is targetSeat or roleIndex in learnedRoles:
                            self.roleGrid[seat][roleIndex] = 0.0

        # for info in knowledge:
        #     targetSeat: int = info.target
        #     learnedRoles: tuple[Role] = info.information

        #     for seat, roles in enumerate(self.roleGrid):
        #         for roleIndex, weight in enumerate(roles):
        #             if seat is targetSeat and roleIndex in learnedRoles:
        #                 self.roleGrid[seat][roleIndex] = 1.0/len(learnedRoles)
        #             elif seat is targetSeat or roleIndex in learnedRoles:
        #                 self.roleGrid[seat][roleIndex] = 0.0

    def buildRoleGrid(self, inScriptRoles: list[Role]):
        playerCount: int = 0
        townsfolkCount: int = 0
        outsiderCount: int = 0
        minionCount: int = 0
        demonCount: int = 0
        inPlayRoles: list[Role] = []

        townsfolk = [role for role in inScriptRoles if isTownsfolk(role)]
        outsiders = [role for role in inScriptRoles if isOutsider(role)]
        minions = [role for role in inScriptRoles if isMinion(role)]
        demons = [role for role in inScriptRoles if isDemon(role)]

        playerCount = [
            knowledge.information
            for knowledge in self.knowledgeBank
            if knowledge.infoType is InfoType.COUNT_PLAYERS
        ][0]

        self.roleGrid = [
            [None for role in inScriptRoles] for seat in range(playerCount)
        ]

        seatsWithInfo: list[Role] = []
        rolesWithInfo: list[Role] = []
        isRoleKnowledge: list[Knowledge] = []

        knownTownsfolk: float = 0.0
        knownOutsider: float = 0.0
        knownMinion: float = 0.0
        knownDemon: float = 0.0

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
                    isRoleKnowledge.append(knowledge)
                    if knowledge.target not in seatsWithInfo:
                        seatsWithInfo.append(knowledge.target)
                        for role in knowledge.information:
                            if isTownsfolk(role):
                                knownTownsfolk += 1 / len(knowledge.information)
                            if isOutsider(role):
                                knownOutsider += 1 / len(knowledge.information)
                            if isMinion(role):
                                knownMinion += 1 / len(knowledge.information)
                            if isDemon(role):
                                knownDemon += 1 / len(knowledge.information)

                    for role in knowledge.information:
                        if role not in rolesWithInfo:
                            rolesWithInfo.append(role)

        if len(isRoleKnowledge) > 0:
            self.__isRole__(
                knowledge=isRoleKnowledge,
                inScriptRoles=inScriptRoles,
                playerCount=playerCount,
            )

        unknownTownsfolk: float = townsfolkCount - knownTownsfolk
        unknownOutsider: float = outsiderCount - knownOutsider
        unknownMinion: float = minionCount - knownMinion
        unknownDemon: float = demonCount - knownDemon

        if Role.BARON in inScriptRoles:
            adjustment = 2.0 * (minionCount / len(minions))
            unknownOutsider += adjustment
            unknownTownsfolk -= adjustment

        if Role.DRUNK in inScriptRoles:
            adjustment = outsiderCount / len(outsiders)
            if Role.BARON in inScriptRoles:
                adjustment += ((outsiderCount + 2) / len(outsiders)) * (
                    minionCount / len(minions)
                )
            unknownOutsider -= adjustment
            unknownTownsfolk += adjustment

        unknownPlayers = playerCount - (
            knownTownsfolk + knownOutsider + knownMinion + knownDemon
        )

        unknownTownsfolk /= unknownPlayers * (len(townsfolk) - knownTownsfolk)
        unknownOutsider /= unknownPlayers * (len(outsiders) - knownOutsider)
        unknownMinion /= unknownPlayers * (len(minions) - knownMinion)
        if (len(demons) - knownDemon) > 0.0 and unknownPlayers > 0.0:
            unknownDemon /= unknownPlayers * (len(demons) - knownDemon)
        else:
            unknownDemon = 0.0

        for seat in range(playerCount):
            if seat in seatsWithInfo:
                continue
            for index, role in enumerate(inScriptRoles):
                if role in rolesWithInfo:
                    continue
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
                target=self.seat,
                infoType=InfoType.IS_ROLE,
                information=[self.role],
            ),
            Knowledge(
                day=0,
                source=None,
                target=None,
                infoType=InfoType.INPLAY_ROLE,
                information=[self.role],
            ),
        ]

        self.learnAndRebuildGrid(inScriptRoles=inScriptRoles, learnedInfo=learnedInfo)
