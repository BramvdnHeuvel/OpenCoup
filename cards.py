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