import random as r
import math as m

from brainHelper import *
from enums.infoType import *
from knowledge import *
from brainPlayer import Player, learnStartingInfo

def main() -> None:
    r.seed(a=0, version=2)
    playerCount = 8
    inScriptRoles = [_ for _ in Role if _ >= Role.WASHERWOMAN]
    roles, drunkRole = getRoles(playerCount)
    players = [
        Player(
            seat=seat,
            role=roles[seat],
            isDrunk=roles[seat] is drunkRole,
            playerCount=playerCount,
        )
        for seat in list(range(playerCount))
    ]

    learnStartingInfo(inScriptRoles=inScriptRoles, players=players)

    targetPlayer = 0
    for role in inScriptRoles:
        sum = 0.0
        for seat in players[targetPlayer].roleGrid:
            sum += seat[role]
            print(f"{seat[role]}")
        print(f"{role.name}: {sum}")

    for seat in range(playerCount):
        print(f"Seat {seat} {roles[seat].name}")

    # for knowledge in players[0].knowledgeBank:
    #     print(knowledge)



if __name__ == "__main__":
    main()
