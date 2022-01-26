lab = [[0] * 1000 for i in range(1000)]

sp = [tuple(map(int, input().split()))]
cur = 0
while sp != []:
    cur += 1
    sp1 = []
    for el in sp:
        point = lab[el[1]][el[0]]
        if point == 0:
            lab[el[1]][el[0]] = cur
        try:
            if lab[el[1] + 1][el[0]] == 0:
                sp1.append((el[0], el[1] + 1))
        except Exception:
            pass
        try:
            if el[1] - 1 > -1 and lab[el[1] - 1][el[0]] == 0:
                sp1.append((el[0], el[1] - 1))
        except Exception:
            pass
        try:
            if lab[el[1]][el[0] + 1] == 0:
                sp1.append((el[0] + 1, el[1]))
        except Exception:
            pass
        try:
            if el[0] - 1 > -1 and lab[el[1]][el[0] - 1] == 0:
                sp1.append((el[0] - 1, el[1]))
        except Exception:
            pass
    sp = list(set(sp1))