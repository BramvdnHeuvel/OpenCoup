from game.objects import NPC, deck, Model
from game.model import new_model
from mechanics.turn import execute_turn
from game.reader import read_model
import random

F = 1/2
PACK_SKIP = 1/25
ROW_SKIP = 1/50

INDIVIDUAL_NOISE = 1/100

def train_model(size=50, generations=2000):
    gen = [new_model() for _ in range(size)]
    gen.append(Model(read_model('models/v2/model7.json')))
    gen.append(Model(read_model('models/v2/model8.json')))
    gen.append(Model(read_model('models/v2/model9.json')))

    for i in range(generations):
        gen = new_generation(gen)

        if i % 100 == 0:
            victor = new_model()
            for challenger in gen:
                victor = two_model_competition(victor, challenger)
            print(victor.data)
            victor.save(f'models/recent/gen-{i}.json')
        print(f"Generation {i} has been reached.")

    # Once the training has finished, pick the best one.
    victor = new_model()
    for challenger in gen:
        victor = two_model_competition(victor, challenger)
    
    print(victor.data)
    return victor

def new_generation(generation):
    size = len(generation)

    for i in range(size):
        parent = generation[i]
        helper_one = parent
        helper_two = parent

        while helper_one is parent:
            helper_one = random.choice(generation)
        while helper_two is parent or helper_two is helper_one:
            helper_two = random.choice(generation)

        child = make_new_child(parent, helper_one, helper_two)
        generation[i] = two_model_competition(parent, child)
    return generation  

def make_new_child(model_zero, model_one, model_two):
    child = new_model()

    for pack in range(len(model_zero.data)):
        if random.random() > PACK_SKIP:
            for i in range(len(model_zero.data[pack])):
                for j in range(len(model_zero.data[pack][i])):
                    if random.random() > ROW_SKIP:
                        for k in range(len(model_zero.data[pack][i][j])):
                            a = model_zero.data[pack][i][j][k][1]
                            b = model_one.data[pack][i][j][k][1]
                            c = model_two.data[pack][i][j][k][1]

                            ta = model_zero.data[pack][i][j][k][0]
                            tb = model_one.data[pack][i][j][k][0]

                            new_value = min(a/2 + F * (b - c), 1000000)
                            new_value = max(new_value, -1000000)

                            new_t_value = ta
                            if random.random() < 0.05:
                                new_t_value = tb
                                if random.random() < 0.2:
                                    new_t_value = random.randint(0,7)

                            child.data[pack][i][j][k] = (new_t_value, new_value)

    return child

def two_model_competition(model_one, model_two):
    bram = NPC(model_one, "Bram")
    mark = NPC(model_two, "Mark")

    victor = execute_turn(bram, mark)
    deck.reset()

    if victor is bram:
        return bram.model
    if victor is mark:
        return mark.model
    if victor is None:
        return bram.model