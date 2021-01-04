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


def makegraph(capacity):
    graph = {}
    for i, values in enumerate(capacity):
        graph[i] = []
        for pos, val in enumerate(values):
            if val > 0:
                graph[i].append(pos)
    return graph, len(graph)


def bfs(capacity, s, t):
    graph, n = makegraph(capacity)
    d = np.array([-1 for i in range(n)])
    d[s] = 0

    visited = []
    queue = []

    visited.append(s)
    queue.append(s)

    while queue:
        v = queue.pop(0)

        for neighbor in graph[v]:
            if neighbor not in visited:
                d[neighbor] = d[v] + 1

                visited.append(neighbor)
                queue.append(neighbor)

    return d[t] != -1, d
    # return d


def dfs(visited, capacity, node, t, flow, d):
    if node == t:
        return flow, capacity

    graph, _ = makegraph(capacity)

    if node not in visited:
        visited.add(node)
        # print(graph[node])
        for neighbor in graph[node]:
            if d[neighbor] != d[node] + 1:
                continue

            # print(node)
            pushed, capacity = dfs(visited, capacity, neighbor, t, min(flow, capacity[node][neighbor]), d)
            if pushed:
                capacity[node][neighbor] = capacity[node][neighbor] - pushed
                capacity[neighbor][node] = capacity[neighbor][node] + pushed
                return pushed, capacity

    return 0, capacity


def dinic(capacity, s, t):
    flow = 0

    logical, d = bfs(capacity, s, t)

    while logical:
        # print('\n', d)
        pushed, capacity = dfs(set(), capacity, s, t, np.inf, d)
        # print(capacity)
        flow = flow + pushed
        logical, d = bfs(capacity, s, t)

    return flow


print(start_cap)
t1 = time.perf_counter()
print('Max flow is: ', dinic(capacity, s, t))
t2 = time.perf_counter()
print("Time elapsed: ", t2 - t1)
