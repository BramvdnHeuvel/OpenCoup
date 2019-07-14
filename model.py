class Model:
    pass

class NPC:
    """An NPC is an instance of a model that is capable of participating in a game.
    
    The NPC requires a model as an input to determine how it makes its choices."""

    def __init__(self, model):
        self.money = 0