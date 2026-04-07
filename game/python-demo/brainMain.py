import random as r
import math as m

from brainHelper import *
from enums.roles import Role
from enums.infoType import *
from knowledge import *
from brainPlayer import Player


def main() -> None:
    r.seed(a=None, version=2)
    playerCount = 12
    inScriptRoles = [_ for _ in Role if _ >= Role.WASHERWOMAN]
    roles, reminderTokens = getRoles(
        playerCount=playerCount, inScriptRoles=inScriptRoles
    )
    players = [
        Player(
            seat=seat,
            role=roles[seat],
            reminderTokens=reminderTokens[seat],
            playerCount=playerCount,
        )
        for seat in list(range(playerCount))
    ]
    for player in players:
        player.learnMyRole(inScriptRoles=inScriptRoles)

    firstNightInfo(players=players, inScriptRoles=inScriptRoles)

    # Debug printing
    # targetPlayer = [player.seat for player in players if isMinion(player.role)][0]
    # playerSum = [0.0 for seat in range(playerCount)]
    # print (f"Seat {targetPlayer}:")
    # for role in inScriptRoles:
    #     roleSum = 0.0
    #     for seatNum, seat in enumerate(players[targetPlayer].roleGrid):
    #         roleSum += seat[role]
    #         playerSum[seatNum] += seat[role]
    #         print(f"{seat[role]:.5f}", end=" ")
    #     print(f"\n{role.name}: {roleSum:.5f}\n")

    # targetPlayer = 0
    # playerSum = [0.0 for seat in range(playerCount)]
    # for role in inScriptRoles:
    #     roleSum = 0.0
    #     for seatNum, seat in enumerate(players[targetPlayer].roleGrid):
    #         roleSum += seat[role]
    #         playerSum[seatNum] += seat[role]
    #         print(f"{seat[role]:.5f}", end=" ")
    #     print(f"\n{role.name}: {roleSum:.5f}\n")

    # for targetPlayer in range(playerCount):
    #     playerSum = [0.0 for seat in range(playerCount)]
    #     for role in inScriptRoles:
    #         roleSum = 0.0
    #         for seatNum, seat in enumerate(players[targetPlayer].roleGrid):
    #             roleSum += seat[role]
    #             playerSum[seatNum] += seat[role]
    #     print(f"Seat {targetPlayer:<6} {players[targetPlayer].role.name:<14}:", end="\t\t")
    #     for seat, player in enumerate(playerSum):
    #         print(f"{player:.5f}", end=" ")
    #     print("")

    # for seat in range(playerCount):
    #     print(f"Seat {seat} {players[seat].role.name}")
    #     print(f"Reminder Tokens: {players[seat].reminderTokens}")

    targetPlayer = [player.seat for player in players if isMinion(player.role)][0]
    for knowledge in players[targetPlayer].knowledgeBank:
        print(knowledge)


def firstNightInfo(players: list[Player], inScriptRoles: list[Role]) -> None:
    # Minions Learn their demon and other minions
    minions = [player for player in players if isMinion(player.role)]
    for minion in minions:
        knowledge: list[Knowledge] = []
        for otherMinion in [_ for _ in minions if _ is not minion]:
            otherMinionSeat = players.index(otherMinion)
            knowledge.append(Knowledge(
                0,
                None,
                otherMinionSeat,
                InfoType.IS_ROLE,
                [Role.BARON, Role.POISONER, Role.SCARLET_WOMAN, Role.SPY],
            ))
        minion.learnAndRebuildGrid(inScriptRoles=inScriptRoles, learnedInfo=knowledge)

    # Demon learns minions and their bluffs
    # Poisoner act
    poisoners = [player for player in players if player.role is Role.POISONER]
    for poisoner in poisoners:
        print("Poisoner Poisons someone")
    # Spys learn their info
    # Washerwoman info
    # Librarian info
    # Investigator info
    # Chef info
    # Empath info
    # Fortune Teller acts
    # Butler acts


if __name__ == "__main__":
    main()
