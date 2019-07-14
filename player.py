from responses import Turns

class Player:
    def __init__(self, card1, card2):
        self.money = 0
        self.cards = [card1, card2]

        self.claims_before_switch = {
            'assassin': 0,
            'contessa': 0,
            'captain': 0,
            'ambassador': 0,
            'duque': 0
        }

        self.claims_after_switch = {
            'assassin': 0,
            'contessa': 0,
            'captain': 0,
            'ambassador': 0,
            'duque': 0
        }

    def take_turn_against(self, opponent):
        """The player makes a choice what move it makes during its turn in the current situation."""
        while True:
            answer = input("Your move: ").lower()

            if answer == 'coup' and self.money >= 7:
                return Turns.coup

            elif self.money < 10:
                if answer == 'draw 1':
                    return Turns.draw_one
                if answer == 'draw 3':
                    return Turns.draw_three
                if answer == 'kill' and self.money >= 3:
                    return Turns.assassinate
                if answer == 'steal':
                    return Turns.steal
                if answer == 'switch':
                    return Turns.switch
    
    def lives(self):
        """Returns the amount of alive cards that the player has left."""
        return len([card for card in self.cards if card.alive])

    def has(self, name):
        """Returns a bool whether the given player has the given card concealed."""
        for card in self.cards:
            if card.type == name and card.alive:
                return True
        return False

    def death(self):
        """Lose an influence due to death."""
        pass #! TODO

    def assassination(self, opponent):
        """Determine whether to allow, contest or block the assassination."""
        pass #! TODO
    
    def contessa_block(self, opponent):
        """Determine whether to allow or contest a contessa block."""
        pass #! TODO
    
    def get_stolen(self, opponent):
        """Determine whether to allow to get stolen by the opponent."""
        pass #! TODO