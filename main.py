from turn import execute_turn
from game.objects import Player

bram = Player("Bram")
mark = Player("Mark")

print(str(execute_turn(bram, mark)))