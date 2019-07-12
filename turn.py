from responses import Turns, Assassination, AllowOrContest, Theft
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
    response = opponent.draw_with_ambassador(player)

    if response == AllowOrContest.contest and not player.has('duque'):
        player.death()
    else:
        if response == AllowOrContest.contest:
            opponent.death()
        
        player.money += 3

def coup(player, opponent):
    player.money += -7
    opponent.death()

def assassinate(player, opponent):
    response = opponent.assassination(player)

    if response == Assassination.allow:
        player.money += -3
        opponent.death()
    
    elif response == Assassination.contest:
        if player.has('assassin'):
            player.money += -3
            opponent.death()
        else:
            player.death()
    
    elif response == Assassination.block:
        player.money += -3
        response2 = player.contessa_block(opponent)

        if response2 == AllowOrContest.allow:
            pass
        else:
            if opponent.has('contessa'):
                player.death()
            else:
                opponent.death()
                opponent.death()

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
            opponent.death()
        else:
            player.death()
    
    elif response == Theft.block_ambassador:
        response2 = player.ambass_block(opponent)

        if response2 == AllowOrContest.allow:
            pass
        else:
            if opponent.has('ambassador'):
                player.death()
            else:
                money = min(opponent.money, 2)

                player.money += money
                opponent.money += -1*money
                opponent.death()
    
    elif response == Theft.block_captain:
        response2 = player.capt_block(opponent)

        if response2 == AllowOrContest.allow:
            pass
        else:
            if opponent.has('captain'):
                player.death()
            else:
                money = min(opponent.money, 2)

                player.money += money
                opponent.money += -1*money
                opponent.death()

def switch(player, opponent):
    response = player.switch_ambassador(opponent)

    if response == AllowOrContest.contest and not player.has('ambassador'):
        player.death()
    else:
        if response == AllowOrContest.contest:
            opponent.death()

        card3 = deck.draw()
        card4 = deck.draw()

        trash_card_1, trash_card_2 = player.choose(card3, card4)
        
        deck.insert(trash_card_1)
        deck.insert(trash_card_2)
