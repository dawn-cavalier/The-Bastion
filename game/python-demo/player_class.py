from enums.roles import *
from enums.characters import *


class Player:
    role: Role
    character: Character
    isAlive: bool
    seat: int
    presence: float
    alignment: Alignment
    reminderTokens: list[tuple[Role, Status]]
    
    knowledgeBank: list
    trust: list[float]
    demonCandidates: list[float]
    evilCandidates: list[float]
    outsiderCandidates: list[float]
    inPlayRoles: list[Role]
    playerRoles: list[list[Role]]

    def __init__(self, character: Character) -> None:
        self.character = character
        self.reset()

    def __str__(self) -> str:
        return (
            f"Character: {self.character.name}\n"
            f"Seat: {self.seat}\n"
            f"Role: {self.role.name}\n"
            f"isAlive: {self.isAlive}\n"
            f"Alignment: {self.alignment.name}\n"
            f"Presence: {self.presence}"
        )

    def reset(self) -> None:
        self.role = Role.NONE
        self.presence = 0.5
        self.seat = -1
        self.isAlive = True
        self.reminderTokens = []
        self.alignment = Alignment.UNASSIGNED

        self.knowledgeBank = []
        self.trust = [0.5 for _ in Character]
        self.demonCandidates = [0.0 for _ in Character]
        self.evilCandidates = [0.0 for _ in Character]
        self.outsiderCandidates = [0.0 for _ in Character]
        self.inPlayRoles = [Role.NONE for _ in Character]
        self.playerRoles = [[] for _ in Character]

    def learn(self, day: int, source: Character, information: any) -> None:
        self.knowledgeBank.append((day, source, information))
 