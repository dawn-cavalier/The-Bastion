from random import shuffle, sample, randint

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


def isNeighbor(numberOfPlayers: int, seat1: int, seat2: int) -> bool:
    diff = abs(seat1 - seat2)
    return diff == 1 or diff == numberOfPlayers - 1


def processNight(day: int, activePlayers: list[Player]) -> None:
    # Cleanup reminder tokens
    tokensToRemove = [
        (Role.BUTLER, Status.IS_MASTER),
        (Role.POISONER, Status.IS_POISONED),
    ]
    for token in tokensToRemove:
        for player in activePlayers:
            if token in player.reminderTokens:
                player.reminderTokens.remove(token)

    if day == 1:
        nightOneOrder(activePlayers)
        return

    nightOrder(day, activePlayers)


def nightOneOrder(activePlayers: list[Player]) -> None:
    day = 1

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
    investigators = [
        player for player in activePlayers if player.role == Role.INVESTIGATOR
    ]
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
    fortuneTellers = [
        player for player in activePlayers if player.role == Role.FORTUNE_TELLER
    ]
    for fortuneTeller in fortuneTellers:
        fortuneTellerActs(fortuneTeller, day, activePlayers)

    # Butler Chooses a Player
    butlers = [player for player in activePlayers if player.role == Role.BUTLER]
    for bulter in butlers:
        bulterActs(bulter, day, activePlayers)


def nightOrder(day: int, activePlayers: list[Player]) -> None:
    posioners = [player for player in activePlayers if player.role == Role.POISONER]
    for posioner in posioners:
        posionerActs(posioner, activePlayers)

    # Monk Acts

    spies = [player for player in activePlayers if player.role == Role.SPY]
    for spy in spies:
        spyActs(spy, day, activePlayers)

    # Scarlet Woman acts

    # Imp Acts

    # Ravenkeeper Acts

    # Undertaker Acts

    # Empath Learns
    empaths = [player for player in activePlayers if player.role == Role.EMPATH]
    for empath in empaths:
        empathActs(empath, day, activePlayers)

    # Fortune Teller Chooses Two Players and Learns
    fortuneTellers = [
        player for player in activePlayers if player.role == Role.FORTUNE_TELLER
    ]
    for fortuneTeller in fortuneTellers:
        fortuneTellerActs(fortuneTeller, day, activePlayers)

    # Butler Chooses a Player
    butlers = [player for player in activePlayers if player.role == Role.BUTLER]
    for bulter in butlers:
        bulterActs(bulter, day, activePlayers)


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


def librarianActs(librarian: Player, day: int, activePlayers: list[Player]) -> None:
    outsiders = [
        player
        for player in activePlayers
        if isOutsider(player.role)
        or (Role.DRUNK, Status.IS_DRUNK) in player.reminderTokens
    ]

    # TODO: Add Drunk Or Poison logic
    if isDrunkOrPoisoned(librarian):
        print("Implement Librarian's misinfo")
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
        f"PLAYER {learnedPlayers[0].character.name} OR PLAYER {learnedPlayers[1].character.name} ARE ROLE {roleLearned.name}",
    )


def investigatorActs(
    investigator: Player, day: int, activePlayers: list[Player]
) -> None:
    # TODO: Add Drunk Or Poison logic
    if isDrunkOrPoisoned(investigator):
        print("Implement Investigator's misinfo")
        return

    # TODO: Better Character Selection
    minions = [player for player in activePlayers if isMinion(player.role)]
    correctPlayer = sample(minions, 1)[0]
    wrongPlayer = sample(
        [
            player
            for player in activePlayers
            if player.character is not correctPlayer.character
            and player.character is not investigator.character
        ],
        1,
    )[0]

    learnedPlayers = [correctPlayer, wrongPlayer]
    shuffle(learnedPlayers)

    investigator.learn(
        day, investigator.character, f"ROLE {correctPlayer.role.name} IS IN PLAY"
    )
    investigator.learn(
        day,
        investigator.character,
        f"PLAYER {learnedPlayers[0].character.name} OR PLAYER {learnedPlayers[1].character.name} ARE ROLE {correctPlayer.role.name}",
    )


def chefActs(chef: Player, day: int, activePlayers: list[Player]) -> None:
    # TODO: Make Recluse logic smarter
    evilSeats = [
        player.seat
        for player in activePlayers
        if (player.alignment is Alignment.EVIL or player.role is Role.RECLUSE)
        and player.role is not Role.SPY
    ]
    numberOfPlayers = len(activePlayers)

    chefNumber = 0
    for seat1 in evilSeats:
        for seat2 in [seat for seat in evilSeats if seat is not seat1]:
            if isNeighbor(numberOfPlayers, seat1, seat2):
                chefNumber += 1
    chefNumber = chefNumber >> 1

    # TODO: Add smarter drunk logic
    if isDrunkOrPoisoned(chef):
        newVal = randint(0, 2)
        while newVal == chefNumber:
            newVal = randint(0, 2)
        chefNumber = newVal

    chef.learn(day, chef.character, f"THERE ARE {chefNumber} PAIRS OF EVIL PLAYERS")


def empathActs(empath: Player, day: int, activePlayers: list[Player]) -> None:
    neighbors = [
        player
        for player in activePlayers
        if isNeighbor(len(activePlayers), empath.seat, player.seat)
    ]

    empathNumber = len(
        [
            player
            for player in neighbors
            if (player.alignment is Alignment.EVIL or player.role is Role.RECLUSE)
            and player.role is not Role.SPY
        ]
    )

    # TODO: Make consistent across nights
    if isDrunkOrPoisoned(empath):
        newVal = randint(0, 2)
        while newVal == empathNumber:
            newVal = randint(0, 2)
        empathNumber = newVal

    empath.learn(
        day,
        empath.character,
        f"BETWEEN PLAYER {neighbors[0].character.name} AND PLAYER {neighbors[1].character.name} THERE ARE {empathNumber} EVIL PLAYERS",
    )


def fortuneTellerActs(
    fortuneTeller: Player, day: int, activePlayers: list[Player]
) -> None:
    # TODO: Add Targeting
    targets = sample(activePlayers, 2)
    demons: list[Player]
    # TODO: Add smarter drunk logic
    if isDrunkOrPoisoned(fortuneTeller):
        demons = [
            player
            for player in targets
            if (Role.FORTUNE_TELLER, Status.IS_RED_HERRING) in player.reminderTokens
            or player is Role.RECLUSE
        ]
    else:
        demons = [
            player
            for player in targets
            if isDemon(player.role)
            or (Role.FORTUNE_TELLER, Status.IS_RED_HERRING) in player.reminderTokens
            or player is Role.RECLUSE
        ]

    if len(demons):
        fortuneTeller.learn(
            day,
            fortuneTeller.character,
            f"PLAYER {targets[0].character.name} OR PLAYER {targets[1].character.name} IS THE DEMON",
        )
        return

    fortuneTeller.learn(
        day,
        fortuneTeller.character,
        f"PLAYER {targets[0].character.name} AND PLAYER {targets[1].character.name} IS NOT THE DEMON",
    )


def bulterActs(bulter: Player, day: int, activePlayers: list[Player]) -> None:
    # TODO: Add targeting logic
    master = sample([player for player in activePlayers if player is not bulter], 1)[0]
    master.reminderTokens.append((Role.BUTLER, Status.IS_MASTER))
