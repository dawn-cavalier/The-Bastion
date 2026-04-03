import random as r
import math as m

from brainHelper import *
from enums.roles import Role
from enums.infoType import *
from knowledge import *
from brainPlayer import Player


def main() -> None:
    r.seed(a=0, version=2)
    playerCount = 8
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
    targetPlayer = 2
    for role in inScriptRoles:
        sum = 0.0
        for seat in players[targetPlayer].roleGrid:
            sum += seat[role]
            print(f"{seat[role]}")
        print(f"{role.name}: {sum}\n")

    # for seat in range(playerCount):
    #     print(f"Seat {seat} {players[seat].role.name}")
    #     print(f"Reminder Tokens: {players[seat].reminderTokens}")

    # for knowledge in players[0].knowledgeBank:
    #     print(knowledge)


def firstNightInfo(players: list[Player], inScriptRoles: list[Role]) -> None:
    # Minions Learn their demon and other minions
    minions = [player for player in players if isMinion(player.role)]
    for minion in minions:
        for otherMinion in [_ for _ in minions if _ is not minion]:
            otherMinionSeat = players.index(otherMinion)
            knowledge = Knowledge(
                0,
                None,
                otherMinionSeat,
                InfoType.IS_ROLE,
                (Role.BARON, Role.POISONER, Role.SCARLET_WOMAN, Role.SPY),
            )
        # minion.learn(inScriptRoles=inScriptRoles, )

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
