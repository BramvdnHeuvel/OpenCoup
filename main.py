from mechanics.turn import execute_turn
from game.objects import Player, NPC
from game.model import new_model

model1 = new_model()
model2 = new_model()

bram = NPC(model1, name="BRAM")
mark = NPC(model2, name="MARK")

print(execute_turn(bram, mark))