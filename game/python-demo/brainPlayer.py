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

        seatsWithInfo = []
        rolesWithInfo = []
        
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
                    self.__isRole__(knowledge=knowledge)
                    if knowledge.target not in seatsWithInfo:
                        seatsWithInfo.append(knowledge.target)
                        if isTownsfolk(knowledge.information):
                            knownTownsfolk += 1
                        if isOutsider(knowledge.information):
                            knownOutsider += 1
                        if isMinion(knowledge.information):
                            knownMinion += 1
                        if isDemon(knowledge.information):
                            knownDemon += 1

                    if knowledge.information not in rolesWithInfo:
                        rolesWithInfo.append(knowledge.information)

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

        unknownPlayers = playerCount - (knownTownsfolk + knownOutsider + knownMinion + knownDemon)

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

        self.learnAndRebuildGrid(inScriptRoles=inScriptRoles, learnedInfo=learnedInfo)
