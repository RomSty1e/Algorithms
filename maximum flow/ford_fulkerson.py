import time

import numpy as np

capacity = np.array([
    [0, 20, 30, 10, 0],
    [0, 0, 40, 0, 30],
    [0, 0, 0, 10, 20],
    [0, 0, 0, 0, 20],
    [0, 0, 0, 0, 0]
])

start_cap = np.copy(capacity)

s = 0
t = 4

c = np.copy(capacity)


def solve(cap, source, tip):
    flow = 0
    cnt = 1

    while len([i for i, val in enumerate(cap[source]) if val > 0]) > 0:

        flow_way = np.array([]).astype(int)
        pos = source

        # print('\n', 'iter :', cnt)
        cnt = cnt + 1

        while pos != tip:
            flow_way = np.append(flow_way, pos)
            next_prob_points = np.array([i for i, val in enumerate(cap[pos]) if val > 0 and i not in flow_way])

            # print('Position now: ', pos + 1)
            # print('Probably next positions :', next_prob_points + 1)

            if len(next_prob_points) > 0:
                max_v = 0
                next_pos = next_prob_points[0]

                for points in next_prob_points:
                    if cap[pos][points] > max_v:
                        max_v = cap[pos][points]
                        next_pos = points

                pos = next_pos
            else:
                if pos != 0:
                    block = pos
                    prev = flow_way[flow_way != block][-1]
                    cap[prev][block] = -1
                    # flow_way = flow_way[flow_way != block]
                    flow_way = flow_way[:-2]
                    pos = prev
                else:
                    break

        flow_way = np.append(flow_way, tip)

        f = np.inf
        for i, point in enumerate(flow_way[:-1]):
            f = min(f, cap[flow_way[i]][flow_way[i + 1]])

        for i, point in enumerate(flow_way[:-1]):
            if cap[flow_way[i]][flow_way[i + 1]] >= 0:
                cap[flow_way[i]][flow_way[i + 1]] = cap[flow_way[i]][flow_way[i + 1]] - f
            if cap[flow_way[i + 1]][flow_way[i]] >= 0:
                cap[flow_way[i + 1]][flow_way[i]] = cap[flow_way[i + 1]][flow_way[i]] + f

        # print('Flow way :', flow_way + 1)
        # print('Flow on this way: ', f)
        # print(cap)

        flow = flow + f

    return flow


print(start_cap)
t1 = time.perf_counter()
print('Max flow is: ', solve(capacity, s, t))
t2 = time.perf_counter()
print("Time elapsed: ", t2 - t1)
