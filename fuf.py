import copy


class A:
    step = 0

class B:
    def __init__(self, data):
        self.data = data

    def func(self):
        self.data.step += 1

a = A()
b = B(copy.deepcopy(a))
b.func()
print(a.step)
print(b.data.step)