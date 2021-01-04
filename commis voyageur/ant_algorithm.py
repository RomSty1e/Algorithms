import random
from math import sqrt

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import time

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

alpha = 1
betta = 1
q = 10
forget = 0.2
num_ants = 1000

pheromone_memory = np.ones((number_of_cities, number_of_cities))


def solve(cities, head, pheromone_memory, num_ants, forget, alpha, betta, q):
    def distance(point1, point2):
        res = sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        if res == 0:
            res = 1000000
        return res

    def way_dist(way, cities):
        way_len = 0
        for i in range(len(way) - 1):
            way_len = way_len + distance(cities[int(way[i])], cities[int(way[i + 1])])
        return way_len

    def transition_probability(cities, way_now, head_now, next_head, eta, pheromone_memory, alpha, betta):
        sum_val = 0
        for num, _ in enumerate(cities):
            if num not in way_now:
                sum_val = sum_val + (eta[head_now][num] ** betta) * (pheromone_memory[head_now][num] ** alpha)

        res = 100 * (eta[head_now][next_head] ** betta) * (
                pheromone_memory[head_now][next_head] ** alpha) / sum_val

        return res

    eta = np.zeros((len(cities), len(cities)))
    for i in range(len(cities)):
        for j in range(len(cities)):
            eta[i][j] = 1 / distance(cities[i], cities[j])

    best_way_len = np.inf
    best_way = np.array([val for val in range(len(cities))])

    for i in range(num_ants):
        pheromone_memory = pheromone_memory * (1 - forget)

        residual_path = np.array([val for val in range(len(cities))])

        way_now = np.array([]).astype(int)

        way_now = np.append(way_now, head)

        residual_path = residual_path[residual_path != head]

        head_now = head

        prob_of_trans = np.zeros((len(cities), len(cities)))

        while len(residual_path) > 0:

            for num, point in enumerate(cities):
                if num not in way_now:
                    prob_of_trans[head_now][num] = transition_probability(cities, way_now, head_now, num, eta,
                                                                          pheromone_memory,
                                                                          alpha, betta)

            tmp_val = 0
            prob_segment = [tmp_val]

            for val in residual_path:
                tmp_val = tmp_val + prob_of_trans[head_now][val]
                prob_segment.append(tmp_val)

            rnd_val = random.randint(1, 100)

            for pos, val in enumerate(prob_segment[:-1]):
                if (rnd_val <= prob_segment[pos + 1]) and (prob_segment[pos] <= rnd_val):
                    head_now = residual_path[pos]
                    break

            # print(prob_segment)

            way_now = np.append(way_now, head_now)

            residual_path = residual_path[residual_path != head_now]

        way_now = np.append(way_now, head)

        delta_memory = q / way_dist(way_now, cities)

        for j in range(len(way_now) - 1):
            pheromone_memory[way_now[j]][way_now[j + 1]] = pheromone_memory[way_now[j]][
                                                               way_now[j + 1]] + delta_memory
            pheromone_memory[way_now[j + 1]][way_now[j]] = pheromone_memory[way_now[j]][
                way_now[j + 1]]

        # pheromone_memory = pheromone_memory + delta_memory

        if way_dist(way_now, cities) < best_way_len:
            best_way_len = way_dist(way_now, cities)
            best_way = way_now

    return best_way, best_way_len


ans_way, ans_way_len = solve(cities, head, pheromone_memory, num_ants, forget, alpha, betta, q)
print('Best way distance: ', ans_way_len)
print('Best way: ', end=' ')
for val in ans_way:
    print(val, end=' ')

x_list = []
y_list = []
for point in ans_way:
    x_list.append(cities[point][0])
    y_list.append(cities[point][1])

fig, ax = plt.subplots()
title_name = 'Муравьи' + '\n' + 'Количетсво городов: ' + str(number_of_cities) + '\n' + 'Путь: ' + str(
    "%.2f" % ans_way_len)
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
