import random
from itertools import permutations
from math import sqrt
import time

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def distance(point1, point2):
    res = sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    if res == 0:
        res = 1000000
    return res


number_of_cities = int(input('Enter quantity of cities: '))

t1 = time.perf_counter()

cities = []
for i in range(number_of_cities):
    point = [random.randint(0, 100) for j in range(2)]
    cities.append(point)

cities = [[49, 46], [43, 59], [95, 8], [50, 77], [32, 14], [27, 27], [70, 0], [36, 50], [100, 9], [67, 60]]

print('All cities: ', cities, '\n')

head = int(input('Enter number of starting city: '))
head = head - 1
print('First city: ', cities[head], '\n')
cities_for_visit = cities[0:head] + cities[head + 1:]

best_distance = 0
tmp_cities = [cities[head]] + cities[0:head] + cities[head + 1:] + [cities[head]]
ans = tmp_cities

for i in range(number_of_cities):
    best_distance = best_distance + distance(tmp_cities[i], tmp_cities[i + 1])
# print('First best way: ', ans)
# print("first best distance: ", best_distance)
# print('\n')

all_ways = []
for i in permutations(cities_for_visit):
    way = [cities[head]] + list(i[:]) + [cities[head]]
    all_ways.append(way)
# print('Quantity of all ways: ', len(all_ways))

for way in all_ways:
    new_distance = 0

    # print('Way: ', way)
    # print('Way: ', way[1:-1])

    for i in range(len(way) - 1):
        new_distance = new_distance + distance(way[i], way[i + 1])
    # print('Distance: ', new_distance)
    # print('\n')
    if new_distance < best_distance:
        best_distance = new_distance
        ans = way

print('Best way: ', ans)
print('Best way distance: ', best_distance)

x_list = []
y_list = []
for point in ans:
    x_list.append(point[0])
    y_list.append(point[1])

fig, ax = plt.subplots()
title_name = 'Полный перебор' + '\n' + 'Количество городов: ' + str(number_of_cities) + '\n' + 'Путь: ' + str(
    "%.2f" % best_distance)
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
print("Time elapsed: ", t2 - t1)

plt.show()
