import random as r
import math as m

from brainHelper import *
from enums.roles import Role
from enums.infoType import *
from knowledge import *
from brainPlayer import Player

def testPrintRoleGrid(targetPlayer: Player):
    for row in targetPlayer.roleGrid:
        for value in row:
            if value is not None:
                print (f"{value:.2f}", end=", ")
            else:
                print (f"{"NONE":<4}", end=", ")
        print ("")

def testPrintTargetGridSums(targetPlayer: Player, playerCount: int, inScriptRoles: list[Role]):
    playerSum = [0.0 for seat in range(playerCount)]
    print(f"Seat {targetPlayer.seat}:")
    for role in inScriptRoles:
        roleSum = 0.0
        for seatNum, seat in enumerate(targetPlayer.roleGrid):
            roleSum += seat[role]
            playerSum[seatNum] += seat[role]
            print(f"{seat[role]:.5f}", end=" ")
        print(f"\n{role.name}: {roleSum:.5f}")


def testPrintAllGridSums(players: list[Player], playerCount: int, inScriptRoles: list[Role]):
    print(f"{"SEAT":<11}{"ROLE":<14}:", end="")
    for seat in range(playerCount):
        print(f" SEAT{seat:<2}", end="")
    print("")
    for targetPlayer in range(playerCount):
        playerSum = [0.0 for seat in range(playerCount)]
        for role in inScriptRoles:
            roleSum = 0.0
            for seatNum, seat in enumerate(players[targetPlayer].roleGrid):
                roleSum += seat[role]
                playerSum[seatNum] += seat[role]
        print(f"Seat {targetPlayer:<6}{players[targetPlayer].role.name:<14}:", end="")
        for seat, player in enumerate(playerSum):
            print(f" {player:.4f}", end="")
        print("")
