from importlib import reload

import gp

reload(gp)

# p1 = gp.makerandomtree(5)
# p2 = gp.makerandomtree(5)
# print(gp.gridgame([p1, p2]))

# reload(gp)
#
winner = gp.evolve(5, 100, gp.tournament, maxgen=50)

gp.gridgame([winner, gp.humanplayer()])
