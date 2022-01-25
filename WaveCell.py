def slice_board(x, y, spis):
    if x == 0 or y == 0:
        print('первая клетка (1;1)!!!')
    else:
        lab_human = spis[y - 1:y + 2]
        for i in range(len(lab_human)):
            lab_human[i] = lab_human[i][x - 1:x + 2]
        return lab_human

def main():
    #lab = [[0] * 7 for _ in range(7)]
    #for el in lab:
    #    print(el)
    lab = [[0, -1, 0, 0, 0, 0, 0],
           [0, -1, 0, 0, 0, 0, 0],
           [0, -1, -1, 0, -1, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, -1, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0]]
    x1, y1 = list(map(int, input().split())) # откуда начинаем идти
    # первая клетка (1;1)!!!
    x1 -= 1
    y1 -= 1
    #x2, y2 = list(map(int, input().split())) # куда идем
    '''
    for yi in range(len(lab)):
        for xi in range(len(lab[0])):
            if lab[yi][xi] == 1:
                lab[yi][xi] = ''
    '''
    slice_board(x1, y1)
    '''finalout = voln(2, 2, 1, 3, 3, lab)
    for el in finalout:
        print(el)'''


def voln(x, y, cur, n, m, lab):
    lab[x][y] = cur
    if y + 1 < m:
        if lab[x][y + 1] == 0 or (lab[x][y + 1] != '' and lab[x][y + 1] > cur):
            voln(x, y + 1, cur + 1, n, m, lab)
    if x + 1 < n:
        if lab[x + 1][y] == 0 or (lab[x + 1][y] != '' and lab[x + 1][y] > cur):
            voln(x + 1, y, cur + 1, n, m, lab)
    if x - 1 >= 0:
        if lab[x - 1][y] == 0 or (lab[x - 1][y] != '' and lab[x - 1][y] > cur):
            voln(x - 1, y, cur + 1, n, m, lab)
    if y - 1 >= 0:
        if lab[x][y - 1] == 0 or (lab[x][y - 1] != '' and lab[x][y - 1] > cur):
            voln(x, y - 1, cur + 1, n, m, lab)
    return lab

main()