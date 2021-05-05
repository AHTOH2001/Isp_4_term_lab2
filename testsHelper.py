CONST = 5


class ClassTest:
    def __init__(self):
        pass

    x = CONST

    def meth(self, y):
        self.x += y
        return self.x


def fn_test(x):
    x += CONST
    x *= 2
    return x
