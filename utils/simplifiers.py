# from types import

# from mypy.types import NoneType
# import NoneType
import inspect
import logging

class Simplifier:

    @classmethod
    def simplify_to_json_supported(cls, obj: object):
        print(__builtins__)
        if isinstance(obj, (type(None), int, float, str, list, tuple, bytes, dict, set)):
            return cls._simplify_simple(obj)
        elif hasattr(obj, '__call__'):
            return cls._simplify_callable(obj)
        else:
            return cls._simplify_complex(obj)

    @classmethod
    def _simplify_simple(cls, simple_obj: object):
        if isinstance(simple_obj, bytes):
            return simple_obj.decode()
        elif isinstance(simple_obj, (list, tuple)):
            return [cls.simplify_to_json_supported(el) for el in simple_obj]
        elif isinstance(simple_obj, dict):
            return dict(
                [(cls.simplify_to_json_supported(key), cls.simplify_to_json_supported(val)) for key, val in simple_obj.items()])
        else:
            return simple_obj

    @classmethod
    def _simplify_callable(cls, fn: object):
        result = {}
        members = dict(inspect.getmembers(fn))
        print(members)
        # for member, member_value in filter(lambda x: inspect.getmembers(fn)):
        #     if member in IMPORTANT_ATTRIBUTES:
        #         dct[member] = serialize_obj(member_value)
        #     if member == "__code__":
        #         dct["__globals__"] = {}
        #         glob = f.__globals__
        #         for name in member_value.co_names:
        #             if name == f.__name__:
        #                 dct["__globals__"][name] = f.__name__
        #             elif not inspect.isbuiltin(name):
        #                 if name in glob:
        #                     if not inspect.ismodule(glob[name]):
        #                         dct["__globals__"][name] = serialize_obj(glob[name])
        # return dct

    @classmethod
    def _simplify_complex(cls, complex_obj: object):


        pass

    # if isinstance(obj, dict):


CONST = 5

def fn_test(x):
    x += CONST
    x = pow(x, 2)
    return x

# obj = {'nine': 9, 'list': [5, 8, None], b'sad': bytes([4, 2, 19, 123]), '1': b'sad'}
# print(obj)
# res = serialize_obj(obj)
res = Simplifier.simplify_to_json_supported(fn_test)
print(res)

# x = b'asf'
# res = Simplifier.simplify_to_json_supported({x: 6})


