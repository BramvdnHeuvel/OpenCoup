from enum import Enum

class Turns(Enum):
    draw_one = 1
    # draw_two = 2
    draw_three = 3

    assassinate = 4
    steal = 5
    switch = 6

    coup = 7

class Assassination(Enum):
    allow = 1
    contest = 2
    block = 3

class AllowOrContest(Enum):
    allow = 1
    contest = 2

class Theft(Enum):
    allow = 1
    contest = 2

    block_captain = 3
    block_ambassador = 4