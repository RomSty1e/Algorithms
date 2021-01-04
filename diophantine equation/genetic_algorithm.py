import random


def solve(popsize, maxiter, dna_size, elite, mut_prob, step):
    '''
    :param popsize: Population size
    :param maxiter: Maximum number of iterations
    :param dna_size: Number of chromosomes
    :param elite: Individuals suitable for mating
    :param mut_prob: The probability of mutation
    :param step: Mutation of a chromosome
    :return: Fitness, set of chromosomes
    '''

    def score(dna):
        result = 30
        val = dna[0] + 2 * dna[1] + 3 * dna[2] + 4 * dna[3]
        return abs(val - result)

    def mutate(dna):
        i = random.randint(0, dna_size - 1)
        if random.random() < 0.5 and dna[i] > 2:
            return dna[0:i] + [dna[i] - step] + dna[i + 1:]
        elif dna[i] < 30:
            return dna[0:i] + [dna[i] + step] + dna[i + 1:]

    def crossover(parent1, parent2):
        i = random.randint(1, dna_size - 1)
        return parent1[0:i] + parent2[i:]

    # First population
    population = []
    for i in range(popsize):
        dna = [random.randint(1, 30) for j in range(dna_size)]
        population.append(dna)

    scores = []

    for i in range(maxiter):
        scores = [(score(dna), dna) for dna in population]
        scores.sort()
        ranked = [dna for (s, dna) in scores]

        top_dna = int(elite * popsize)
        population = ranked[0:top_dna]

        while len(population) < popsize:
            if random.random() < mut_prob:
                c = random.randint(0, top_dna)
                population.append(mutate(ranked[c]))
            else:
                p1 = random.randint(0, top_dna)
                p2 = random.randint(0, top_dna)
                population.append(crossover(ranked[p1], ranked[p2]))

        if scores[0][0] == 0:
            return scores[0]

    return -1


popsize = 50
maxiter = 1000
dna_size = 4
elite = 0.25
mut_prob = 0.2
step = 1

ans = solve(popsize, maxiter, dna_size, elite, mut_prob, step)

if ans == -1:
    print('No solution found.')
else:
    print('Solution: ', ans[1])
