import random


class Player:
    def __init__(self, x, y, direction, wasHit, score) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.wasHit = wasHit
        self.score = score

DIRECTIONS = ["F","R", "L"] 

def get_throw(myself: Player, opponent: Player):
    if myself.x - opponent.x == 0:
        if myself.y > opponent.y and myself.direction ==  "F":
            return "T"
    elif myself.y - opponent.y == 0:
        if myself.x > opponent.x and myself.direction == "L":
            return "T"
        elif myself.direction == "R":
            return "T"
    
    return None


def defend_or_move(myself: Player, opponent: Player):
    if get_throw(myself=opponent, opponent=myself):
        if (opponent.score - myself.score < 3 and opponent.direction == "T") or opponent.wasHit: 
            # attack mode
            if myself.x - opponent.x == 0:
                if myself.y > opponent.y:
                    return "F"
            if myself.y - opponent.y == 0:
                if myself.x > opponent.x:
                    return "L"
                else:
                    return "R"
        else:
            # move - defend mode
            if myself.x - opponent.x == 0:
                if myself.y > opponent.y:
                    return "R"
            if myself.y - opponent.y == 0:
                if myself.x > opponent.x:
                    return "F"
                else:
                    return "F"

    else: # move - attack mode
        if myself.x - opponent.x == 0:
            if myself.y > opponent.y:
                return "F"
            else:
                return None
        if myself.y - opponent.y == 0:
            if myself.x > opponent.x:
                return "L"
            else:
                return "R"
    return DIRECTIONS[random.randrange(len(DIRECTIONS))]