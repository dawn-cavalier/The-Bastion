from enums.infoType import *

class Knowledge:
    day: int
    source: int | None
    target: int | None
    infoType: InfoType
    information: any

    def __init__(
        self,
        day: int,
        source: int | None,
        target: int | None,
        infoType: InfoType,
        information: any,
    ):
        self.day = day
        self.source = source
        self.target = target
        self.infoType = infoType
        self.information = information

    def __str__(self) -> str:
        if self.infoType is InfoType.IS_ROLE:
            if self.source is None:
                return f"On day {self.day}, learned Seat {self.target} {self.infoType.name} {self.information} from the Storyteller."
            return f"On day {self.day}, learned Seat {self.target}  {self.infoType.name} {self.information} from Seat {self.source}."

        if self.infoType in (InfoType.INPLAY_ROLE,):
            return f"On day {self.day}, learned {self.information} is in play."

        if self.infoType in (
            InfoType.COUNT_TOWNSFOLK,
            InfoType.COUNT_OUTSIDERS,
            InfoType.COUNT_MINIONS,
            InfoType.COUNT_DEMONS,
            InfoType.COUNT_PLAYERS,
        ):
            return (
                f"On day {self.day}, learned {self.infoType.name} is {self.information}"
            )
        return f"UNHANDLED {self.infoType.name}"
