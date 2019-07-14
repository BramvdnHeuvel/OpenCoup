from mechanics.responses import Turns, Assassination, AllowOrContest, Theft
from game.objects import deck

def execute_turn(player, opponent, turn_no=1):
    """Continue (or start off) the game by having `player` take a turn against `opponent`."""
    if player.lives() <= 0:
        return opponent
    if opponent.lives() <= 0:
        return player
    if turn_no > 100:
        return None

    turn = player.take_turn_against(opponent)
    turn_no += 1

    if turn == Turns.assassinate:
        assassinate(player, opponent)
    elif turn == Turns.coup:
        coup(player, opponent)
    elif turn == Turns.draw_one:
        draw_one(player, opponent)
    elif turn == Turns.draw_three:
        draw_three(player, opponent)
    elif turn == Turns.steal:
        steal(player, opponent)
    elif turn == Turns.switch:
        switch(player, opponent)
    
    return execute_turn(opponent, player)


def draw_one(player, opponent):
    player.money += 1

def draw_three(player, opponent):
    response = opponent.draw_with_duque(player)

    if response == AllowOrContest.contest and not player.has('duque'):
        player.death(opponent)
    else:
        if response == AllowOrContest.contest:
            opponent.death(player)
        
        player.money += 3

def coup(player, opponent):
    player.money += -7
    opponent.death(player)

def assassinate(player, opponent):
    response = opponent.assassination(player)

    if response == Assassination.allow:
        player.money += -3
        opponent.death(player)
    
    elif response == Assassination.contest:
        if player.has('assassin'):
            player.money += -3
            opponent.death(player)
            opponent.death(player)
        else:
            player.death(opponent)
    
    elif response == Assassination.block:
        player.money += -3
        response2 = player.contessa_block(opponent)

        if response2 == AllowOrContest.allow:
            pass
        else:
            if opponent.has('contessa'):
                player.death(opponent)
            else:
                opponent.death(player)
                opponent.death(player)

def steal(player, opponent):
    response = opponent.get_stolen(player)

    if response == Theft.allow:
        money = min(opponent.money, 2)

        player.money += money
        opponent.money += -1*money
    
    elif response == Theft.contest:
        if player.has('captain'):
            money = min(opponent.money, 2)

            player.money += money
            opponent.money += -1*money
            opponent.death(player)
        else:
            player.death(opponent)
    
    elif response == Theft.block_ambassador:
        response2 = player.ambass_block(opponent)

        if response2 == AllowOrContest.allow:
            pass
        else:
            if opponent.has('ambassador'):
                player.death(opponent)
            else:
                money = min(opponent.money, 2)

                player.money += money
                opponent.money += -1*money
                opponent.death(player)
    
    elif response == Theft.block_captain:
        response2 = player.capt_block(opponent)

        if response2 == AllowOrContest.allow:
            pass
        else:
            if opponent.has('captain'):
                player.death(opponent)
            else:
                money = min(opponent.money, 2)

                player.money += money
                opponent.money += -1*money
                opponent.death(player)

def switch(player, opponent):
    response = opponent.switch_ambassador(player)

    if response == AllowOrContest.contest and not player.has('ambassador'):
        player.death(opponent)
    else:
        if response == AllowOrContest.contest:
            opponent.death(player)

        card3 = deck.draw()
        card4 = deck.draw()

        trash_card_1, trash_card_2 = player.choose(card3, card4, opponent)
        
        deck.insert(trash_card_1)
        deck.insert(trash_card_2)
