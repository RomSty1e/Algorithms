import random
import numpy as np
from itertools import permutations
from math import sqrt
import time

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

number_of_cities = int(input('Enter quantity of cities: '))

t1 = time.perf_counter()

cities = []
for i in range(number_of_cities):
    point = [random.randint(0, 100) for j in range(2)]
    cities.append(point)

cities = [[49, 46], [43, 59], [95, 8], [50, 77], [32, 14], [27, 27], [70, 0], [36, 50], [100, 9], [67, 60]]

print('All cities: \n', cities)

head = int(input('Enter number of starting city: '))
head = head - 1
print('Starting city: ', cities[head], '\n')

cities = np.array(cities)


def solve(all_city, head_pos, pop_size, max_gen):
    def key_func(item):
        return item[0]

    def distance(point1, point2):
        res = sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        if res == 0:
            res = 1000000
        return res

    def way_distance(way):
        way_len = 0
        for i in range(len(way) - 1):
            way_len = way_len + distance(way[i], way[i + 1])
        return way_len

    def mutate(way):
        if random.random() < 0.8:
            first_p = random.randint(1, len(way) - 1)
            second_p = random.randint(first_p, len(way) - 1)

            way[first_p:second_p] = np.flip(way[first_p:second_p], axis=0)
        else:
            first_p = random.randint(1, len(way) - 1)
            second_p = random.randint(first_p, len(way) - 1)
            third_p = random.randint(second_p, len(way) - 1)

            way[first_p:second_p] = np.flip(way[first_p:second_p], axis=0)
            way[second_p:third_p] = np.flip(way[second_p:third_p], axis=0)

        return way

    def create_way(all_city, head_pos):
        way = np.copy(all_city)
        tmp_head = np.copy(way[head_pos])
        way = np.delete(way, head_pos, axis=0)

        # way = mutate(way)
        np.random.shuffle(way)

        way = np.insert(way, 0, tmp_head, axis=0)
        way = np.insert(way, len(way), tmp_head, axis=0)
        # print(way)

        return way

    def create_population(all_city, head_pos, pop_size):
        population = np.array([])

        for _ in range(pop_size):
            way = create_way(all_city, head_pos)
            population = np.append(population, way)
            # population = np.insert(population, len(population), way, axis=0)

        population = population.reshape(pop_size, len(way), 2)
        return population

    population = create_population(all_city, head_pos, pop_size)

    # for way in population:
    #     print(way_distance(way))

    scores = []

    for i in range(max_gen):
        scores = [(way_distance(way), way) for way in population]

        scores.sort(key=key_func)

        ranked = [dna for (s, dna) in scores]
        top_dna = int(0.2 * pop_size)
        population = ranked[0:top_dna]

        while len(population) < pop_size:
            c = random.randint(0, top_dna)
            population.append(mutate(np.array(ranked[c])))

    # print(scores[0])
    return scores[0][0], scores[0][1]


population_size = 50
max_generations = 1000

ans_dist, ans = solve(cities, head, population_size, max_generations)
print('Best way distance: ', ans_dist)
print('Best way: ', end=' ')
for val in ans:
    print(val, end=' ')
# print(ans)

x_list = []
y_list = []
for point in ans:
    x_list.append(point[0])
    y_list.append(point[1])

fig, ax = plt.subplots()
title_name = 'Генетика' + '\n' + 'Количетсво городов: ' + str(number_of_cities) + '\n' + 'Путь: ' + str(
    "%.2f" % ans_dist)
plt.title(title_name)

ax.plot(x_list, y_list, label='ways')

ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))

ax.grid(which='major',
        color='black')
ax.minorticks_on()
ax.grid(which='minor',
        color='gray',
        linestyle=':')

ax.scatter(x_list[0], y_list[0], color='black', s=100, marker='o', label='First city')
ax.scatter(x_list[1:-1], y_list[1:-1], color='orange', s=50, marker='o', label='Other cities')
ax.legend()

fig.set_figwidth(12)
fig.set_figheight(8)

t2 = time.perf_counter()
print('\n', "Time elapsed: ", t2 - t1)

plt.show()
