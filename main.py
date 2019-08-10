from training.genetic import train_model
from game.objects import Player, NPC, Model
from mechanics.turn import execute_turn
from game.reader import read_model
from game.model import new_model

bram = Player("Bram")
enemy = Model(read_model('models/v2/model9.json'))

print(execute_turn(bram, NPC(enemy, "OpenCoup")))