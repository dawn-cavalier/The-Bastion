from enums.roles import Role
from enums.characters import Character


class Player:
    character: Character
    _knownRole: Role
    _trueRole: Role
    seat: int

    presence: float
    trust: list[float]
    roleList: list[tuple]

    def __init__(self, character: Character) -> None:
        self.character = character
        self.reset()

    def __str__(self) -> str:
        return (
            f"Character: {self.character.name}\n"
            f"Seat: {self.seat}\n"
            f"True Role: {self._trueRole.name}\n"
            f"Known Role: {self._knownRole.name}\n"
            f"Presence: {self.presence}"
        )

    def reset(self) -> None:
        self.presence = 0.5
        self.seat = -1
        self._knownRole = Role.NONE
        self._trueRole = Role.NONE
        self.trust = [0.5 for _ in Character]
        self.roleList = [() for _ in Character]

    def setTrueRole(self, newRole: Role) -> None:
        self._trueRole = newRole

    def setKnownRole(self, newRole: Role) -> None:
        self._knownRole = newRole
        self.roleList[self.character] = (newRole,)
