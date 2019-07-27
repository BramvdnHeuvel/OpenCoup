from game.reader import write_model
import random

def matrix_functions():
    def multiply(node, edge):
        return node*edge
    def compare(node, edge):
        return int(node > edge)
    def add(node, edge):
        return node+edge
    def force_equal(node, edge):
        return int(node == edge)
    def down_scale(node, edge):
        return abs(node * edge)**0.2
    def switch(node, edge):
        if node < edge:
            return -1*node*edge
        return node*edge
    def edge_only(node, edge):
        return edge
    def node_only(node, edge):
        return node

    return [multiply, compare, add, force_equal, down_scale, switch, edge_only, node_only]
FUNC = matrix_functions()

class Model:
    def __init__(self, data):
        self.data = data
        self.functions = FUNC

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

    def save(self, file_name='models/recent/last-training.json'):
        write_model(self, file_name)
        return

    def take_matrix(self, n):
        def calculate_variable(vector):
            for i in range(3):
                new_vector = []

                for row in self.data[n][i]:
                    total = 0
                    for tupel, i in zip(row, vector):
                        func = self.functions[tupel[0]%len(FUNC)]
                        total += func(i, tupel[1])
                    total = max(total, 0)
                    new_vector.append(total)
                
                vector = new_vector
            return new_vector
        return calculate_variable

def new_model() -> Model:
    """Create a new random Model that can play Coup."""
    def create_random_matrix(rows, columns=32):
        def make_matrix(amount):
            def rand():
                return 30*random.random() - 15
            return [[(random.randint(0,len(FUNC)-1), rand()) for _ in range(columns)] for _ in range(amount)]
        return [make_matrix(columns), make_matrix(columns), make_matrix(rows)]
    
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
