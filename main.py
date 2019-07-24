from training.genetic import train_model
from game.objects import Player, NPC, Model
from mechanics.turn import execute_turn
from game.reader import read_model

bram = Player("Bram")
enemy = Model(read_model('models/v1/model1.json'))

print(execute_turn(bram, NPC(enemy2, "OpenCoup")))