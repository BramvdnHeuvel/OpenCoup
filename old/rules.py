from responses import Turns, Assassination, AllowOrContest, Theft
from player import Player
from cards import Card

def execute_turn(player=Player(Card("Assassin"), Card("Contessa")), opponent=Player(Card("Captain"), Card("Duque")), turn=1):
    """Execute a turn in the game.  

    The `player` is the one making the turn, while `opponent` is waiting for their own turn.
    
    The `turn` maximum puts a limit to the games, preventing infinite loops."""

    if turn > 50:
        return None

    turn = player.take_turn_against(opponent)

    if turn == Turns.draw_one:
        player.money += 1
        return execute_turn(opponent, player, turn+1)

    if turn == Turns.coup:
        player.money += -7
        opponent.death()

        if opponent.lives() > 0:
            return execute_turn(opponent, player, turn+1)
        # If the opponent died, return the winner.
        return player

    if turn == Turns.assassinate:
        response = opponent.assassination(player)

        if response == Assassination.allow:
            player.money += -3
            opponent.death()
        
        if response == Assassination.contest:
            if player.has('assassin'):
                player.money += -3
                opponent.death()
            else:
                player.death()
        
        if response == Assassination.block:
            player.money += -3
            response2 = player.contessa_block(opponent)

            if response2 == AllowOrContest.allow:
                pass
            else:
                if opponent.has('contessa'):
                    player.death()
                else:
                    opponent.death()
                    if opponent.lives() > 0:
                        opponent.death()
        
        if opponent.lives() <= 0:
            return player
        if player.lives() <= 0:
            return opponent
        return execute_turn(opponent, player, turn+1)
    
    if turn == Turns.steal:
        response = opponent.get_stolen(player)

        if response == Theft.allow:
            money = min(opponent.money, 2)

            player.money += money
            opponent.money += -1*money
        
        if response == Theft.contest:
            if player.has('captain'):
                money = min(opponent.money, 2)

                player.money += money
                opponent.money += -1*money
                opponent.death()
            else:
                player.death()
        
        if response == Theft.block_ambassador:
            pass #! TODO
        