# Magic number
init 0 python:
    class Player:
        def __init__(self, id: int, character: Character):
            self.id = id
            self.character = character

            self._presence = 0.5

        def decreasePresence(self, amount: float) -> None:
            self._presence -= amount
            if self._presence < 0.0:
                self._presence = 0.0

        def increasePresence(self, amount: float) -> None:
            self._presence += amount
            if self._presence > 1.0:
                self._presence = 1.0
        
    class AIPlayer(Player):
        def __init__(self, id: int, character: Character):
            super.__init__(id, character)

