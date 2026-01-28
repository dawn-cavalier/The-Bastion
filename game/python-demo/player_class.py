from enums.roles import Role
from enums.characters import Character


class Player:
    role: Role
    character: Character
    seat: int
    presence: float
    trust: list[float]

    reminderTokens: list[tuple[Role, any]]    

    def __init__(self, character: Character) -> None:
        self.character = character
        self.reset()

    def __str__(self) -> str:
        return (
            f"Character: {self.character.name}\n"
            f"Seat: {self.seat}\n"
            f"Role: {self.role.name}\n"
            f"Presence: {self.presence}"
        )

    def reset(self) -> None:
        self.role = Role.NONE
        self.presence = 0.5
        self.seat = -1
        self.trust = [0.5 for _ in Character]
        self.reminderTokens = []

 