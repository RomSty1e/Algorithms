def solve():
    def check(a, b, c, d):
        if a + 2 * b + 3 * c + 4 * d == 30:
            return True
        else:
            return False

    ans = []

    for a in range(1, 31):
        for b in range(1, 31):
            for c in range(1, 31):
                for d in range(1, 31):
                    if check(a, b, c, d):
                        one_ans = [a] + [b] + [c] + [d]
                        ans.append(one_ans)

    return ans


solutions = solve()
for sol in solutions:
    print(sol)
