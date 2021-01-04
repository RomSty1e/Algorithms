import time
from math import sin, sinh, sqrt

import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate


def lmbd(n):
    return (np.pi * n) ** 2


def A_n(n):
    def func(x):
        return 1 * sin(sqrt(lmbd(n)) * x)

    return integrate.quad(func, 0, 1)[0]


def B_n(n):
    def func(x):
        return 0 * sin(sqrt(lmbd(n))) * x

    return integrate.quad(func, 0, 1)[0]


def C_n(n):
    def func(y):
        return 1 * sin(sqrt(lmbd(n)) * y)

    return integrate.quad(func, 0, 1)[0]


def D_n(n):
    def func(y):
        return 0 * sin(sqrt(lmbd(n))) * y

    return integrate.quad(func, 0, 1)[0]


def u_1(x, y):
    sum = 0
    for n in range(1, 100):
        sum = sum + 2 * (A_n(n) * (sinh(y * sqrt(lmbd(n)))) / (sinh(sqrt(lmbd(n)))) + B_n(n) * (
            sinh((1 - y) * sqrt(lmbd(n)))) / (sinh(sqrt(lmbd(n))))) * sin(sqrt(lmbd(n)) * x)

    return sum


def u_2(x, y):
    sum = 0
    for n in range(1, 100):
        sum = sum + 2 * (C_n(n) * (sinh(x * sqrt(lmbd(n)))) / (sinh(sqrt(lmbd(n)))) + D_n(n) * (
            sinh((1 - x) * sqrt(lmbd(n)))) / (sinh(sqrt(lmbd(n))))) * sin(sqrt(lmbd(n)) * y)

    return sum


def solution(x, y):
    return u_1(x, y) + u_2(x, y)


size = int(input('Введите размер сетки: '))

t1 = time.perf_counter()

x_array = np.linspace(0, 1, size)
y_array = np.linspace(0, 1, size)

ans = []
for i in range(size):
    tmp = []
    for j in range(size):
        tmp.append(solution(x_array[i], y_array[j]))
    ans.append(tmp)

fig, ax = plt.subplots()

ax.contourf(x_array, y_array, ans)
ax.set_title('Analytical Solution')

cs = ax.contour(x_array, y_array, ans)
ax.clabel(cs, colors='red')

fig.set_figwidth(6)
fig.set_figheight(6)

t2 = time.perf_counter()
print("Time elapsed: ", t2 - t1)

plt.show()
