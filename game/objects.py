from responses import Turns, Assassination, AllowOrContest, Theft
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
                    self.claim('duque')
                    return Turns.draw_three
                if answer == 'kill' and self.money >= 3:
                    self.claim('assassin')
                    return Turns.assassinate
                if answer == 'steal':
                    self.claim('captain')
                    return Turns.steal
                if answer == 'switch':
                    self.claim('ambassador')
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

        if [card for card in self.cards if card.alive] == []:
            self.print("You were killed once more, but that doesn't matter! You were dead anyway.")
            return

        self.print(f"Oh no! You lost a life! Choose one.")
        for card in self.cards:
            if card.alive:
                self.print(card.type)

        while True:
            response = input(f"{self.name} Which card shall you eliminate?")

            for card in self.cards:
                if response == card.type and card.alive:
                    card.alive = False
                    self.print(f"You have eliminated your {card.type}.")
                    return

    def assassination(self, opponent):
        """Determine whether to allow, contest or block the assassination."""
        self.print("Oh no! You're being assassinated!'")
        while True:
            response = input(f"{self.name}: What will you do? (allow/contest/block)")
            if response == 'allow':
                return Assassination.allow
            if response == 'contest':
                return Assassination.contest
            if response == 'block':
                self.claim('contessa')
                return Assassination.block
    
    def contessa_block(self, opponent):
        """Determine whether to allow or contest a contessa block."""
        self.print("Your opponent claims they can block the assassination with a contessa.")
        while True:
            response = input(f"{self.name}: Do you believe them? (believe/call out)")
            if response == 'believe':
                return AllowOrContest.allow
            if response == 'call out':
                return AllowOrContest.contest
    
    def get_stolen(self, opponent):
        """Determine whether to allow to get stolen by the opponent."""
        self.print("Your opponent claims they can steal money from you with their captain.")
        while True:
            response = input(f"{self.name}: Do you believe them? (believe/call out/ambassador/captain)")
            if response == 'believe':
                return Theft.allow
            if response == 'call out':
                return Theft.contest
            if response == 'ambassador':
                self.claim('ambassador')
                return Theft.block_ambassador
            if response == 'captain':
                self.claim('captain')
                return Theft.block_captain
    
    def draw_with_duque(self, opponent):
        """Determine whether to allow that the opponent draws 3 ton with a duque."""
        self.print("Your opponent claims they can earn 3 ton with their duque.")
        while True:
            response = input(f"{self.name}: Do you believe them? (believe/call out)")
            if response == 'believe':
                return AllowOrContest.allow
            if response == 'call out':
                return AllowOrContest.contest
    
    def capt_block(self, opponent):
        """Determine whether to believe that your steal attempt has been blocked by a captain."""
        self.print("Your opponent claims they can block your theft with their captain.")
        while True:
            response = input(f"{self.name}: Do you believe them? (believe/call out)")
            if response == 'believe':
                return AllowOrContest.allow
            if response == 'call out':
                return AllowOrContest.contest
    
    def ambass_block(self, opponent):
        """Determine whether to believe that your steal attempt has been blocked by a captain."""
        self.print("Your opponent claims they can block your theft with their ambassador.")
        while True:
            response = input(f"{self.name}: Do you believe them? (believe/call out)")
            if response == 'believe':
                return AllowOrContest.allow
            if response == 'call out':
                return AllowOrContest.contest
    
    def switch_ambassador(self, opponent):
        """Determine whether to allow that the opponent refreshes their cards with an ambassador."""
        self.print("Your opponent claims they can switch their cards with their ambassador.")
        while True:
            response = input(f"{self.name}: Do you believe them? (believe/call out)")
            if response == 'believe':
                return AllowOrContest.allow
            if response == 'call out':
                return AllowOrContest.contest
    
    def claim(self, name):
        self.claims_after_switch[name] += 1
        self.claims_before_switch[name] += 1
    
    def choose(self, card3, card4):
        cards = [card for card in self.cards if card.alive]
        cards.extend([card3, card4])

        for card in cards:
            self.print(card.type)

        trash1 = None
        trash2 = None

        while True:
            response = input(f"{self.name}: What's the first card you'll put back into the deck?")
            for card in cards:
                if response == card.type:
                    trash1 = card
                    break
            if trash1 is not None:
                break
        while True:
            response = input(f"{self.name}: What's the second card you'll put back into the deck?")
            for card in cards:
                if response == card.type:
                    trash2 = card
                    break
            if trash1 is not None:
                break
                
        cards.remove(trash1)
        cards.remove(trash2)
        self.cards = [card for card in self.cards if not card.alive]
        self.cards.extend(cards)

        self.claims_after_switch = {
            'assassin': 0,
            'contessa': 0,
            'captain': 0,
            'ambassador': 0,
            'duque': 0
        }

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