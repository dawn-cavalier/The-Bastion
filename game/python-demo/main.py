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
    evilPlayers = [
        player for player in activePlayers if player.alignment == Alignment.EVIL
    ]
    goodPlayers = [
        player for player in activePlayers if player.alignment == Alignment.GOOD
    ]

    for evilPlayer in evilPlayers:
        for player in goodPlayers:
            evilPlayer.learn(
                day,
                Character.STORYTELLER,
                f"PLAYER {player.character.name} ALIGNMENT IS {Alignment.GOOD.name}",
            )
        otherEvils = [
            evil for evil in evilPlayers if evil.character != evilPlayer.character
        ]

        for otherEvil in otherEvils:
            name = otherEvil.character.name
            evilPlayer.learn(
                day,
                Character.STORYTELLER,
                f"PLAYER {name} ALIGNMENT IS {Alignment.EVIL.name}",
            )
            if isMinion(otherEvil.role):
                evilPlayer.learn(
                    day,
                    Character.STORYTELLER,
                    f"PLAYER {name} CATEGORY IS MINION",
                )
            if isDemon(otherEvil.role):
                evilPlayer.learn(
                    day,
                    Character.STORYTELLER,
                    f"PLAYER {name} CATEGORY IS DEMON",
                )

    # Demon Learns Bluffs
    demons = [player for player in activePlayers if isDemon(player.role)]
    for demon in demons:
        inPlayTownRoles = [
            player.role for player in activePlayers if isVillager(player.role)
        ]

        notInPlayTownRoles = [
            role
            for role in Role
            if role not in inPlayTownRoles
            and isVillager(role)
            and role is not Role.DRUNK
        ]

        # TODO: Smarter Bluff Selection Logic
        bluffs = sample(notInPlayTownRoles, 3)
        for bluff in bluffs:
            demon.learn(day, Character.STORYTELLER, f"ROLE {bluff.name} IS NOT IN PLAY")

    # Poisoner Posions a Character
    posioners = [player for player in activePlayers if player.role == Role.POISONER]
    for posioner in posioners:
        # TODO: Use the posioner's knowledge instead of activePlayers
        targets = [
            player for player in activePlayers if player.alignment == Alignment.GOOD
        ]
        # TODO: Add targeting logic and player logic
        # First night might as well be random as there is no information
        target = sample(targets, 1)[0]
        target.reminderTokens.append((Role.POISONER, Status.IS_POISONED))

    # Spy Learns the Grimoire
    tests = [player for player in activePlayers if player.role == Role.SPY]
    for test in tests:
        # Drunk or Poisoned Spies don't get to see the Grimoire
        if isDrunkOrPoisoned(test):
            continue

        for player in activePlayers:
            test.learn(
                day,
                test.character,
                f"PLAYER {player.character.name} IS ROLE {player.role.name}",
            )
            test.learn(
                day,
                test.character,
                f"PLAYER {player.character.name} IS ALIGNMENT {player.alignment.name}",
            )
            for _, status in player.reminderTokens:
                test.learn(
                    day,
                    test.character,
                    f"PLAYER {player.character.name} HAS STATUS {status.name}",
                )

    # Washerwoman Learns
    washerwomen = [
        player for player in activePlayers if player.role == Role.WASHERWOMAN
    ]
    for washerwoman in washerwomen:
        # TODO: Implement smarter drunk logic
        if isDrunkOrPoisoned(washerwoman):
            roleLearned = sample(
                [
                    role
                    for role in Role
                    if isVillager(role) and role is not Role.WASHERWOMAN
                ],
                1,
            )[0]
            playersLearned = sample(
                [
                    player
                    for player in activePlayers
                    if player is not washerwoman and player is not roleLearned
                ],
                2,
            )
            washerwoman.learn(
                day, washerwoman.character, f"ROLE {roleLearned.name} IS IN PLAY"
            )
            washerwoman.learn(
                day,
                washerwoman.character,
                f"PLAYER {playersLearned[0].character.name} OR PLAYER {playersLearned[1].character.name} ARE ROLE {roleLearned.name}",
            )
            continue

        # TODO: More intelligent player selection
        correctPlayer = sample(
            [
                player
                for player in activePlayers
                if isTownsfolk(player.role)
                and player.character is not washerwoman.character
            ],
            1,
        )[0]
        wrongPlayer = sample(
            [
                player
                for player in activePlayers
                if player.character is not correctPlayer.character
                and player.character is not washerwoman.character
            ],
            1,
        )[0]
        learnedPlayers = [correctPlayer, wrongPlayer]
        shuffle(learnedPlayers)

        washerwoman.learn(
            day, washerwoman.character, f"ROLE {correctPlayer.role.name} IS IN PLAY"
        )
        washerwoman.learn(
            day,
            washerwoman.character,
            f"PLAYER {learnedPlayers[0].character.name} OR PLAYER {learnedPlayers[1].character.name} ARE ROLE {correctPlayer.role.name}",
        )

    # Librarian Learns
    librarians = [player for player in activePlayers if player.role == Role.LIBRARIAN]
    for librarian in librarians:
        # TODO: Add Drunk Or Poison logic
        if isDrunkOrPoisoned(librarian):
            continue

        outsiders = [
            player
            for player in activePlayers
            if isOutsider(player.role)
            or (Role.DRUNK, Status.IS_DRUNK) in player.reminderTokens
        ]

        if len(outsiders) == 0:
            librarian.learn(day, librarian.character, f"{Role.DRUNK} IS NOT IN PLAY")
            librarian.learn(day, librarian.character, f"{Role.BUTLER} IS NOT IN PLAY")
            librarian.learn(day, librarian.character, f"{Role.SAINT} IS NOT IN PLAY")
            librarian.learn(day, librarian.character, f"{Role.RECLUSE} IS NOT IN PLAY")
            # TODO: Make dynamic based on starting outsider count
            librarian.learn(day, librarian.character, f"{Role.BARON} IS NOT IN PLAY")
            continue

        # TODO: Make smarter player selection logic
        correctPlayer = sample(outsiders, 1)[0]
        wrongPlayer = sample(
            [
                player
                for player in allPlayers
                if player is not correctPlayer and player is not librarian
            ],
            1,
        )[0]
        learnedPlayers = [correctPlayer, wrongPlayer]
        shuffle(learnedPlayers)

        roleLearned = correctPlayer.role
        if (Role.DRUNK, Status.IS_DRUNK) in correctPlayer.reminderTokens:
            roleLearned = Role.DRUNK

        librarian.learn(day, librarian.character, f"ROLE {roleLearned.name} IS IN PLAY")
        librarian.learn(
            day,
            librarian.character,
            f"PLAYER {learnedPlayers[0].character.name} OR PLAYER {learnedPlayers[1].character.name} ARE {roleLearned.name}",
        )

    # Investigator Learns
    # Chef Learns
    # Empath Learns
    # Fortune Teller Chooses Two Players and Learns
    # Butler Chooses a Player

    # Debug printing
    # for character in activePlayers:
    #     print(f"{character}")
    #     if len(character.reminderTokens):
    #         print("Reminder Tokens:")
    #         for token in character.reminderTokens:
    #             print(f"{token}")
    #     print("")

    tests = [player for player in activePlayers if player.role == Role.LIBRARIAN]
    for test in tests:
        print(test.reminderTokens)
        print(test.knowledgeBank)
    ## Start Game


if __name__ == "__main__":
    main()
