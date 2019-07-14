from responses import Turns
import random

class Card:
    def __init__(self, name):
        self.alive = True
        self.type = name.lower()
    
    def data(self):
        if self.alive:
            alive = 1
        else:
            alive = 0
        
        cards = {
            'assassin': 1,
            'contessa': 2,
            'captain': 3,
            'ambassador': 4,
            'duque': 5
        }

        return (cards[self.type], alive)

class Player:
    def __init__(self, name):
        self.money = 0
        self.name = name
        self.cards = [deck.draw(), deck.draw()]

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
    
    def __repr__(self):
        return f"<Player {self.name} | {[card.type for card in self.cards if card.alive]}>"

    def __str__(self):
        text = f"{self.name} -> Money : {self.money}\n"
        text += f"{self.name} -> Your cards: {[(card.type, card.alive) for card in self.cards]}\n"
        text += f"{self.name} -> Claims before switch : {self.claims_before_switch}\n"
        text += f"{self.name} -> Claims after switch : {self.claims_after_switch}\n"
        return text

    def print(self, text):
        print(f"{self.name}: {text}")

    def take_turn_against(self, opponent):
        """The player makes a choice what move it makes during its turn in the current situation."""
        
        self.print("=========================")
        self.print("        YOUR TURN        ")
        self.print("=========================")
        print(str(self))
        print(str(opponent))

        while True:
            answer = input(f"{self.name}: Your move: ").lower()

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
        self.print("Oh no! You lost a life! Choose one.")


    def assassination(self, opponent):
        """Determine whether to allow, contest or block the assassination."""
        pass #! TODO
    
    def contessa_block(self, opponent):
        """Determine whether to allow or contest a contessa block."""
        pass #! TODO
    
    def get_stolen(self, opponent):
        """Determine whether to allow to get stolen by the opponent."""
        pass #! TODO
    
    def draw_with_duque(self, opponent):
        """Determine whether to allow that the opponent draws 3 ton with a duque."""
        pass #! TODO
    
    def capt_block(self, opponent):
        """Determine whether to believe that your steal attempt has been blocked by a captain."""
        pass #! TODO
    
    def ambass_block(self, opponent):
        """Determine whether to believe that your steal attempt has been blocked by a captain."""
        pass #! TODO
    
    def switch_ambassador(self, opponent):
        """Determine whether to allow or contest an ambassador switch."""
        pass #! TODO
    
    def claim(self, name):
        self.claims_after_switch[name] += 1
        self.claims_before_switch[name] += 1
    
    def choose(self, card3, card4):
        cards = [card for card in self.cards if card.alive].extend([card3, card4])

        pass #! TODO: Choose two bad cards that must be thrown back into the deck.
        trash1 = None
        trash2 = None

        return trash1, trash2

class Model:
    pass

class NPC:
    """An NPC is an instance of a model that is capable of participating in a game.
    
    The NPC requires a model as an input to determine how it makes its choices."""

    def __init__(self, model):
        self.money = 0

class Deck:
    def __init__(self):
        self.cards = {
            'assassin': 3,
            'contessa': 3,
            'captain': 3,
            'ambassador': 3,
            'duque': 3
        }
        self.length = 15
    
    def draw(self):
        i = 0
        drawn = random.randint(1, self.length)

        for name in self.cards:
            i += self.cards[name]
            if i >= drawn:
                self.length += -1
                self.cards[name] += -1
                return Card(name)
        raise IndexError("Deck had invalid preset length.")
    
    def insert(self, card):
        self.cards[card.type] += 1

deck = Deck()