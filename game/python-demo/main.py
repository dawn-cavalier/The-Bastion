from random import shuffle, sample

from player_class import Player
from enums.roles import Role, Alignment, Status
from enums.characters import Character
from helper import *


def main() -> None:
    ## Macro Game Setup
    allPlayers = [
        Player(character)
        for character in Character
        if character >= Character.POV and character <= Character.BLACK
    ]

    ## Micro Game Setup
    activePlayers = sample([player for player in allPlayers], 10)
    activePlayers = buildGame(activePlayers)

    ## Night 1
    day = 1
    # Minions Learn Minions
    # Minions Learn Demon
    # Demon Learns Minions
    evilLearnsEachOther(day, activePlayers)
    demonLearnsBluffs(day, activePlayers)

    # Poisoner Posions a Character
    posioners = [player for player in activePlayers if player.role == Role.POISONER]
    for posioner in posioners:
        posionerActs(posioner, activePlayers)

    # Spy Learns the Grimoire
    spies = [player for player in activePlayers if player.role == Role.SPY]
    for player in spies:
        spyActs(player, day, activePlayers)

    # Washerwoman Learns
    washerwomen = [
        player for player in activePlayers if player.role == Role.WASHERWOMAN
    ]
    for washerwoman in washerwomen:
        washerwomanActs(washerwoman, day, activePlayers)

    # Librarian Learns
    librarians = [player for player in activePlayers if player.role == Role.LIBRARIAN]
    for librarian in librarians:
        librarianActs(librarian, day, activePlayers)

    # Investigator Learns
    investigators = [player for player in activePlayers if player.role == Role.INVESTIGATOR]
    for investigator in investigators:
        investigatorActs(investigator, day, activePlayers)

    # Chef Learns
    chefs = [player for player in activePlayers if player.role == Role.CHEF]
    for chef in chefs:
        chefActs(chef, day, activePlayers)

    # Empath Learns
    empaths = [player for player in activePlayers if player.role == Role.EMPATH]
    for empath in empaths:
        empathActs(empath, day, activePlayers)

    # Fortune Teller Chooses Two Players and Learns
    fortuneTellers = [player for player in activePlayers if player.role == Role.FORTUNE_TELLER]
    for fortuneTeller in fortuneTellers:
        fortuneTellerActs(fortuneTeller, day, activePlayers)

    # Butler Chooses a Player
    butlers = [player for player in activePlayers if player.role == Role.BUTLER]
    for bulter in butlers:
        bulterActs(bulter, day, activePlayers)

    # Debug printing
    # for character in activePlayers:
    #     print(f"{character}")
    #     if len(character.reminderTokens):
    #         print("Reminder Tokens:")
    #         for token in character.reminderTokens:
    #             print(f"{token}")
    #     print("")

    for player in [player for player in activePlayers]:
        print(f"{player.character.name}: {player.role.name}")
        print("Reminder Tokens:")
        print(player.reminderTokens)
        print("Knowledge Bank:")
        print(player.knowledgeBank)
        print("")
    ## Start Game


if __name__ == "__main__":
    main()
