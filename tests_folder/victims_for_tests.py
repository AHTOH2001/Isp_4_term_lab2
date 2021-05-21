import collections

CONST = 5


class ClassTest:
    def __init__(self):
        pass

    x = CONST

    def meth(self, y):
        self.x += y
        return self.x


def simple_fn(y=10):
    return y


def fn_with_pow_and_sf(x):
    x += CONST
    x = pow(x, 2)
    return x + simple_fn()


def fibonachi(n):
    if n <= 2:
        return 1
    else:
        return fibonachi(n - 1) + fibonachi(n - 2)


def fn_with_builtin():
    return collections.deque()
