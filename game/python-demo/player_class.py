from enums.roles import Role
from enums.characters import Character

class Player():
    presence: float
    character: Character
    role: Role
    seat: int
    trust: list

    def __init__(self, character: Character) -> None:
        self.character = character
        self.reset()

    def __str__(self) -> str:
        return f"Character: {self.character.name}\nSeat: {self.seat}\nRole: {self.role.name}\nPresence: {self.presence}"
    
    def reset(self) -> None:
        self.presence = 0.5
        seat = -1
        role = Role.NONE
        trust = (0.5 for _ in Character)