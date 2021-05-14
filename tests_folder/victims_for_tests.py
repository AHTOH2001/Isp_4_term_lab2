CONST = 5


class ClassTest:
    def __init__(self):
        pass

    x = CONST

    def meth(self, y):
        self.x += y
        return self.x


def fn_hren(y=10):
    return y


def fn_test(x):
    x += CONST
    x = pow(x, 2)
    return x + fn_hren()


def fibonachi(n):
    if n <= 2:
        return 1
    else:
        return fibonachi(n - 1) + fibonachi(n - 2)
