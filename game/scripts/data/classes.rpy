# Magic number
init 0 python:
    class Player:
        def __init__(self, id: int, character: Character):
            self.id = id
            self.character = character

            self._presence = 0.5
            # Magic Number
            self._doubt = (0.0 for _ in range(6))

        def decreasePresence(self, amount: float) -> None:
            self._presence -= amount
            if self._presence < 0.0:
                self._presence = 0.0

        def increasePresence(self, amount: float) -> None:
            self._presence += amount
            if self._presence > 1.0:
                self._presence = 1.0
        
        def getPresence(self) -> float:
            return self._presence

        def getDoubt(self, id: int) -> float:
            return self._doubt[id]

