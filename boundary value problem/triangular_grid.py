import os
import time

import matplotlib.pyplot as plt
import numpy as np

num_triangular = int(input('Введите число треугольников 36, 440 или 3912: '))

points_info_path = '.\\' + os.path.join(str(num_triangular), 'fp.txt')
triangular_info_path = '.\\' + os.path.join(str(num_triangular), 'ft.txt')

data_points = np.genfromtxt(points_info_path, delimiter='')
data_triangulars = np.genfromtxt(triangular_info_path, delimiter='').astype(int)

data_triangulars = data_triangulars - 1
# print(data_triangulars)

triangulars = {}

for i, data in enumerate(data_triangulars):
    triangulars[i] = {
        'id': i,
        'points': [data[0], data[1], data[2]],
        'center': {
            'x': (data_points[data[0]][0] + data_points[data[1]][0] + data_points[data[2]][0]) / 3,
            'y': (data_points[data[0]][1] + data_points[data[1]][1] + data_points[data[2]][1]) / 3
        },
        'u_value': 0,
        'neighbors': [j for j, triangle in enumerate(data_triangulars) if
                      len(list(set(data[:-1]) & set(triangle[:-1]))) == 2],
    }

for i, _ in enumerate(triangulars):
    if len(triangulars[i]['neighbors']) == 2:

        ny = 0
        nx = 0

        for point in triangulars[i]['points']:
            if data_points[point][0] == 1:
                nx = nx + 1
            if data_points[point][1] == 1:
                ny = ny + 1

            if nx == 2 or ny == 2:
                triangulars[i]['boundary value'] = 1
            else:
                triangulars[i]['boundary value'] = 0

num_iter = int(input('Введите число итераций: '))
t1 = time.perf_counter()

next_triangulars = triangulars
for _ in range(num_iter):
    triangulars = next_triangulars

    for i, triangle in enumerate(triangulars):
        if (len(triangulars[i]['neighbors'])) == 3:
            next_triangulars[i]['u_value'] = (triangulars[triangulars[i]['neighbors'][0]]['u_value'] +
                                              triangulars[triangulars[i]['neighbors'][1]]['u_value'] +
                                              triangulars[triangulars[i]['neighbors'][2]]['u_value']) / 3
        else:
            next_triangulars[i]['u_value'] = (triangulars[triangulars[i]['neighbors'][0]]['u_value'] +
                                              triangulars[triangulars[i]['neighbors'][1]]['u_value'] +
                                              triangulars[i]['boundary value']) / 3

# for i, _ in enumerate(triangulars):
#     print(triangulars[i])

x = []
y = []
u = []

for i, _ in enumerate(triangulars):
    x.append(triangulars[i]['center']['x'])
    y.append(triangulars[i]['center']['y'])
    u.append(triangulars[i]['u_value'])

fig, ax = plt.subplots()

ax.tricontourf(x, y, u)
ax.set_title('Triangular Grid')

# fig.colorbar(ax.contourf(x_array, y_array, ans), ax=ax)

cs = ax.tricontour(x, y, u)
ax.clabel(cs, colors='red')

fig.set_figwidth(6)
fig.set_figheight(6)

t2 = time.perf_counter()
print("Time elapsed: ", t2 - t1)

plt.show()
