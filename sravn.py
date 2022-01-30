steps = {"Right_Walk": [f"Right_Walk/{i}.png" for i in range(4)],
         "Left_Walk": [f"Left_Walk/{i}.png" for i in range(4)],
         "Up_Walk": [f"Up_Walk/{i}.png" for i in range(4)],
         "Down_Walk": [f"Down_Walk/{i}.png" for i in range(4)]}
tile_size = 30
index =

def update():
    global tile_size, index, rect_x, ost, image
    if index == 4:
        # self.direction()
        if direction() == "Right_Walk":
            ost = tile_size - rect_x
            # удвоенный остаток от картинки слева и справа
            index = 1
            image = steps[direction()][0]
            # так и должно быть))
    else:
        move = ost // (4 - index)  # более точный расчёт, чтобы точно проходил от середины до середины
        rect_x += move
        ost -= move
        image = steps[direction()][index]
        index += 1


def direction():
    return "Right_Walk"
