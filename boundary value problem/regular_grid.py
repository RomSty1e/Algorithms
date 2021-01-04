import time

import matplotlib.pyplot as plt
import numpy as np


def solve(size, error, num_iter):
    u = np.zeros((size, size))

    u[:, u.shape[1] - 1] = 1
    u[u.shape[0] - 1, :] = 1
    u[:, 0] = 0
    u[0, :] = 0

    next_u = np.copy(u)

    for i in range(1, u.shape[0] - 1):
        for j in range(1, u.shape[1] - 1):
            next_u[i][j] = 0.25 * (next_u[i - 1][j] + u[i + 1][j] + u[i][j + 1] + next_u[i][j - 1])

    max_error = np.max(np.fabs(u - next_u))

    if num_iter == 0:
        while max_error > error:
            u = np.copy(next_u)
            next_u = np.copy(u)

            for i in range(1, u.shape[0] - 1):
                for j in range(1, u.shape[1] - 1):
                    next_u[i][j] = 0.25 * (next_u[i - 1][j] + u[i + 1][j] + u[i][j + 1] + next_u[i][j - 1])

            max_error = np.max(np.fabs(u - next_u))
    else:
        for _ in range(num_iter):
            u = np.copy(next_u)
            next_u = np.copy(u)

            for i in range(1, u.shape[0] - 1):
                for j in range(1, u.shape[1] - 1):
                    next_u[i][j] = 0.25 * (next_u[i - 1][j] + u[i + 1][j] + u[i][j + 1] + next_u[i][j - 1])

    return u


size = int(input('Введите размер сетки: '))
error = 0.00001
num_iter = int(input('Введите число итераций (введите 0 для автоматического определения числа итераций): '))

t1 = time.perf_counter()

ans = solve(size, error, num_iter)

x_array = np.linspace(0, 1, size)
y_array = np.linspace(0, 1, size)

fig, ax = plt.subplots()

ax.contourf(x_array, y_array, ans)
ax.set_title('Regular Grid')

# fig.colorbar(ax.contourf(x_array, y_array, ans), ax=ax)

cs = ax.contour(x_array, y_array, ans)
ax.clabel(cs, colors='red')

fig.set_figwidth(6)
fig.set_figheight(6)

t2 = time.perf_counter()
print("Time elapsed: ", t2 - t1)

plt.show()
