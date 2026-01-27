from player_class import Player
from enums.roles import Role
from enums.characters import Character

def main() -> None:
    # Create Players
    allPlayers = (Player(character) for character in Character)
    for player in allPlayers:
        print(f"{player}\n")
    
    allRoles = (role for role in Role)
    
    return


if __name__ == "__main__":
    main()