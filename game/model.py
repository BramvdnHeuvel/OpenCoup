import random

class Model:
    def __init__(self, data):
        self.data = data

        self.take_turn = self.take_matrix(0)
        self.choose_death = self.take_matrix(1)
        self.judge_getting_killed = self.take_matrix(2)
        self.judge_contessa_block = self.take_matrix(3)
        self.judge_getting_stolen = self.take_matrix(4)
        self.judge_drawing_duque = self.take_matrix(5)
        self.judge_blocking_captain = self.take_matrix(6)
        self.judge_blocking_ambassador = self.take_matrix(7)
        self.judge_switching_ambassador = self.take_matrix(8)
        self.choose_ambassador_cards = self.take_matrix(9)

    def take_matrix(self, n):
        def calculate_variable(values):
            new_vector = []

            for row in self.data[n]:
                total = 0
                for m, i in zip(row, values):
                    total += m*i
                new_vector.append(total)
            
            return new_vector
        return calculate_variable

def new_model():
    """Create a new random Model that can play Coup."""
    def create_random_matrix(rows, columns=32):
        def rand():
            return 30*random.random() - 15
        return [[rand() for _ in range(columns)] for _ in range(rows)]
    
    turn = create_random_matrix(6)
    death = create_random_matrix(2)
    kill = create_random_matrix(3)
    cont = create_random_matrix(2)
    theft = create_random_matrix(4)
    duque = create_random_matrix(2)
    capt = create_random_matrix(2)
    amba = create_random_matrix(2)
    switch = create_random_matrix(2)
    choose = create_random_matrix(4)

    data = [turn, death, kill, cont, theft, duque, capt, amba, switch, choose]
    return Model(data)