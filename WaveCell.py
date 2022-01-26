def main():
    lab = [[0, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0]]
    for yi in range(len(lab)):
        for xi in range(len(lab[0])):
            if lab[yi][xi] == 1:
                lab[yi][xi] = -1
    rdl = list(map(int, input().split()))
    x1 = rdl[0] - 1
    y1 = rdl[1] - 1
    rdl = list(map(int, input().split()))
    x2 = rdl[0]
    y2 = rdl[1]
    for el in [[0] * (450 // 30) for _ in range(450 // 30)]:
        print(el)
    finalout = voln(7, 6, 1, 13, 13, [[0] * 15 for _ in range(15)])
    for el in finalout:
        print(el)


def voln(x, y, cur, n, m, lab):
    lab[x][y] = cur
    if y + 1 < m:
        if lab[x][y + 1] == 0 or (lab[x][y + 1] != -1 and lab[x][y + 1] > cur):
            voln(x, y + 1, cur + 1, n, m, lab)
    if x + 1 < n:
        if lab[x + 1][y] == 0 or (lab[x + 1][y] != -1 and lab[x + 1][y] > cur):
            voln(x + 1, y, cur + 1, n, m, lab)
    if x - 1 >= 0:
        if lab[x - 1][y] == 0 or (lab[x - 1][y] != -1 and lab[x - 1][y] > cur):
            voln(x - 1, y, cur + 1, n, m, lab)
    if y - 1 >= 0:
        if lab[x][y - 1] == 0 or (lab[x][y - 1] != -1 and lab[x][y - 1] > cur):
            voln(x, y - 1, cur + 1, n, m, lab)
    return lab


main()