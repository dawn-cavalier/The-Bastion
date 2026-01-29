from enums.roles import Role, Alignment, Status
from enums.characters import Character


class Player:
    role: Role
    character: Character
    seat: int
    presence: float
    trust: list[float]
    alignment: Alignment
    reminderTokens: list[tuple[Role, Status]]
    knowledgeBank: list

    def __init__(self, character: Character) -> None:
        self.character = character
        self.reset()

    def __str__(self) -> str:
        return (
            f"Character: {self.character.name}\n"
            f"Seat: {self.seat}\n"
            f"Role: {self.role.name}\n"
            f"Alignment: {self.alignment.name}\n"
            f"Presence: {self.presence}"
        )

    def reset(self) -> None:
        self.role = Role.NONE
        self.presence = 0.5
        self.seat = -1
        self.trust = [0.5 for _ in Character]
        self.reminderTokens = []
        self.alignment = Alignment.UNASSIGNED
        self.knowledgeBank = []

    def learn(self, day: int, source: Character, information: any) -> None:
        self.knowledgeBank.append((day, source, information))
 