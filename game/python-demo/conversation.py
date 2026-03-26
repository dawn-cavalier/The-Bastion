from random import shuffle, sample, randint

from player_class import Player
from enums.roles import Role, Alignment, Status
from enums.characters import Character

def announce(info, day: int, speaker: Player, audience: list[Player]):
    for member in audience:
        member.learn(day, speaker.character, info)


