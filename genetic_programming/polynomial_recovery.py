import gp
from importlib import reload

reload(gp)
rf = gp.getrankfunction(gp.buildhiddenset())
gp.evolve(2, 500, rf, mutationrate=0.2, breedingrate=0.1, pexp=0.5, pnew=0.1)
