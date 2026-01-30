from random import shuffle, sample

from player_class import Player
from enums.roles import Role, Alignment, Status
from enums.characters import Character


def buildGame(allPlayers: list[Player]) -> list[Player]:
    ## Micro Game Setup
    # Clear previous game
    for player in allPlayers:
        player.reset()

    # Get characters who are playing the game
    # TODO: Assumes all players are active players
    activeCharacters = [character for character in allPlayers]

    # Assign Seats
    seats = sample(
        [seat for seat in range(len(activeCharacters))], len(activeCharacters)
    )
    for index, seat in enumerate(seats):
        activeCharacters[index].seat = seat

    assignRoles(activeCharacters)

    return activeCharacters


def assignRoles(characters: list[Player]) -> None:
    # TODO: Dynamic assignment
    # Fill Bag
    townsfolkCount = 7
    outsiderCount = 0
    minionCount = 2
    demonCount = 1

    # TODO: Assumes all roles active
    activeRoles = [role for role in Role]

    # TODO: More intelligently select roles
    townsfolk = sample(
        [role for role in activeRoles if isTownsfolk(role)],
        townsfolkCount,
    )
    outsiders = sample(
        [role for role in activeRoles if isOutsider(role)],
        outsiderCount,
    )
    minions = sample(
        [role for role in activeRoles if isMinion(role)],
        minionCount,
    )
    demons = sample(
        [role for role in activeRoles if isDemon(role)],
        demonCount,
    )

    setupModifyingRoles = [Role.BARON]
    activeSetupModifyingRoles = set(minions) & set(setupModifyingRoles)

    if len(activeSetupModifyingRoles) > 0:
        if Role.BARON in activeSetupModifyingRoles:
            townsfolk.pop()
            townsfolk.pop()
            outsiders += sample(
                [
                    role
                    for role in activeRoles
                    if role >= Role.BUTLER
                    and role <= Role.DRUNK
                    and role not in outsiders
                ],
                2,
            )

    roleBag: list[Role] = townsfolk + outsiders + minions + demons

    # Assign Roles
    shuffle(roleBag)
    for index, role in enumerate(roleBag):
        characters[index].role = role
        if role in (townsfolk + outsiders):
            characters[index].alignment = Alignment.GOOD
        else:
            characters[index].alignment = Alignment.EVIL

    # Assign Reminder Tokens
    for character in characters:
        if character.role == Role.DRUNK:
            knownRole = sample(
                [
                    role
                    for role in activeRoles
                    if role >= Role.WASHERWOMAN
                    and role <= Role.MAYOR
                    and role not in townsfolk
                ],
                1,
            )[0]
            character.role = knownRole
            character.reminderTokens.append((Role.DRUNK, Status.IS_DRUNK))
        if character.role == Role.FORTUNE_TELLER:
            # TODO: Smarter Red Herring Logic
            redHerring = sample(
                [
                    character
                    for character in characters
                    if character.alignment == Alignment.GOOD
                ],
                1,
            )[0]
            redHerring.reminderTokens.append(
                (Role.FORTUNE_TELLER, Status.IS_RED_HERRING)
            )

    # Sort by Seat Number
    characters.sort(key=lambda character: character.seat)


def isVillager(role: Role) -> bool:
    return role >= Role.WASHERWOMAN and role <= Role.DRUNK


def isTownsfolk(role: Role) -> bool:
    return role >= Role.WASHERWOMAN and role <= Role.MAYOR


def isOutsider(role: Role) -> bool:
    return role >= Role.BUTLER and role <= Role.DRUNK


def isMinion(role: Role) -> bool:
    return role >= Role.POISONER and role <= Role.SCARLET_WOMAN


def isDemon(role: Role) -> bool:
    return role >= Role.IMP and role <= Role.IMP


def isDrunkOrPoisoned(player: Player) -> bool:
    for _, status in player.reminderTokens:
        if status == Status.IS_POISONED or status == Status.IS_DRUNK:
            return True
    return False


def evilLearnsEachOther(day: int, activePlayers: list[Player]) -> None:
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


def demonLearnsBluffs(day: int, activePlayers: list[Player]) -> None:
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


def posionerActs(posioner: Player, activePlayers: list[Player]) -> None:
    # TODO: Use the posioner's knowledge instead of activePlayers
    targets = [player for player in activePlayers if player.alignment == Alignment.GOOD]
    # TODO: Add targeting logic and player logic
    # First night might as well be random as there is no information
    target = sample(targets, 1)[0]
    target.reminderTokens.append((Role.POISONER, Status.IS_POISONED))


def spyActs(spy: Player, day: int, activePlayers: list[Player]) -> None:
    # Drunk or Poisoned Spies don't get to see the Grimoire
    if isDrunkOrPoisoned(spy):
        return

    for player in activePlayers:
        spy.learn(
            day,
            spy.character,
            f"PLAYER {player.character.name} IS ROLE {player.role.name}",
        )
        spy.learn(
            day,
            spy.character,
            f"PLAYER {player.character.name} IS ALIGNMENT {player.alignment.name}",
        )
        for _, status in player.reminderTokens:
            spy.learn(
                day,
                spy.character,
                f"PLAYER {player.character.name} HAS STATUS {status.name}",
            )


def washerwomanActs(washerwoman: Player, day: int, activePlayers: list[Player]) -> None:
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
        return

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


def librarianActs(librarian, day, activePlayers) -> None:
    outsiders = [
        player
        for player in activePlayers
        if isOutsider(player.role)
        or (Role.DRUNK, Status.IS_DRUNK) in player.reminderTokens
    ]

    # TODO: Add Drunk Or Poison logic
    if isDrunkOrPoisoned(librarian):

        return

    if len(outsiders) == 0:
        # TODO: For loop?
        librarian.learn(day, librarian.character, f"{Role.DRUNK.name} IS NOT IN PLAY")
        librarian.learn(day, librarian.character, f"{Role.BUTLER.name} IS NOT IN PLAY")
        librarian.learn(day, librarian.character, f"{Role.SAINT.name} IS NOT IN PLAY")
        librarian.learn(day, librarian.character, f"{Role.RECLUSE.name} IS NOT IN PLAY")
        # TODO: Make dynamic based on starting outsider count
        librarian.learn(day, librarian.character, f"{Role.BARON.name} IS NOT IN PLAY")
        return

    # TODO: Make smarter player selection logic
    correctPlayer = sample(outsiders, 1)[0]
    wrongPlayer = sample(
        [
            player
            for player in activePlayers
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
