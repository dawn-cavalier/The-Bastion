# import random as r
# import math as m

from brainHelper import *
from enums.roles import Role
# from enums.infoType import *
# from knowledge import *
from brainPlayer import Player
from brainTest import *


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
    # targetPlayer = [player for player in players if isDemon(player.role)][0]
    # testPrintRoleGrid(targetPlayer=targetPlayer)

    # targetPlayer = [player for player in players if isMinion(player.role)][0]
    # testPrintTargetGridSums(targetPlayer=targetPlayer, playerCount=playerCount, inScriptRoles=inScriptRoles)

    # targetPlayer = [player.seat for player in players if isDemon(player.role)][0]
    # testPrintTargetGridSums(targetPlayer=targetPlayer, playerCount=playerCount, inScriptRoles=inScriptRoles)

    # targetPlayer = players[0]
    # testPrintTargetGridSums(targetPlayer=targetPlayer, playerCount=playerCount, inScriptRoles=inScriptRoles)

    # targetPlayer = [player for player in players if isMinion(player.role)][0]
    # inPlayRoles = targetPlayer.__getKnownInPlayRoles__(inScriptRoles=inScriptRoles)
    # print (inPlayRoles)

    # targetPlayer = [player.seat for player in players if isMinion(player.role)][0]
    # notInPlayRoles = players[targetPlayer].__getNotInPlayRoles__(inScriptRoles=inScriptRoles)
    # print (notInPlayRoles)

    # targetPlayer = [player.seat for player in players if isMinion(player.role)][0]
    # knownPlayers = players[targetPlayer].__getKnownPlayers__(inScriptRoles=inScriptRoles)
    # print (knownPlayers)

    # testGridSums(players=players, playerCount=playerCount, inScriptRoles=inScriptRoles)

    # for seat in range(playerCount):
    #     print(f"Seat {seat} {players[seat].role.name}")
    #     print(f"Reminder Tokens: {players[seat].reminderTokens}")

    # targetPlayer = [player.seat for player in players if isDemon(player.role)][0]
    # for knowledge in players[targetPlayer].knowledgeBank:
    #     print(knowledge)


def firstNightInfo(players: list[Player], inScriptRoles: list[Role]) -> None:
    playerRoles = [player.role for player in players]
    notInPlayRoles = [role for role in inScriptRoles if role not in playerRoles]
    bluffableRoles = [
        role
        for role in notInPlayRoles
        if (isTownsfolk(role) or isOutsider(role)) and role is not Role.DRUNK
    ]

    minions = [player for player in players if isMinion(player.role)]
    demons = [player for player in players if isDemon(player.role)]

    # Minions Learn their demon and other minions
    for minion in minions:
        knowledge: list[Knowledge] = []
        knowledge.append(
            Knowledge(
                0,
                None,
                [
                    otherMinion.seat
                    for otherMinion in minions
                    if otherMinion.seat != minion.seat
                ],
                InfoType.IS_ROLE,
                [Role.BARON, Role.POISONER, Role.SCARLET_WOMAN, Role.SPY],
            )
        )
        minion.learnAndRebuildGrid(inScriptRoles=inScriptRoles, learnedInfo=knowledge)

    # Demon learns minions and bluffs
    for demon in demons:
        knowledge: list[Knowledge] = []
        # Minions
        knowledge.append(
            Knowledge(
                0,
                None,
                [minion.seat for minion in minions],
                InfoType.IS_ROLE,
                [Role.BARON, Role.POISONER, Role.SCARLET_WOMAN, Role.SPY],
            )
        )
        # Bluffs
        knowledge.append(
            Knowledge(
                0,
                None,
                [player.seat for player in players],
                InfoType.IS_NOT_ROLE,
                r.sample(bluffableRoles, 3),
            )
        )
        demon.learnAndRebuildGrid(inScriptRoles=inScriptRoles, learnedInfo=knowledge)

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
