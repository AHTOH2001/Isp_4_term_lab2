# from types import

# from mypy.types import NoneType
# import NoneType
import inspect
import types
import logging
import builtins


class Simplifier:

    @classmethod
    def simplify_to_json_supported(cls, obj: object):
        if isinstance(obj, (type(None), int, float, str, list, tuple, bytes, dict, set)):
            return cls._simplify_simple(obj)
        elif hasattr(obj, '__code__'):
            return cls._simplify_function(obj)
        else:
            return cls._simplify_complex(obj)

    @classmethod
    def _simplify_simple(cls, simple_obj: object):
        if isinstance(simple_obj, bytes):
            # return simple_obj.decode()
            return list(simple_obj)
        elif isinstance(simple_obj, (list, tuple, set)):
            return [cls.simplify_to_json_supported(el) for el in simple_obj]
        elif isinstance(simple_obj, dict):
            return dict(
                [(cls.simplify_to_json_supported(key), cls.simplify_to_json_supported(val)) for key, val in
                 simple_obj.items()])
        else:
            return simple_obj

    @classmethod
    def _simplify_function(cls, fn: object):
        members = dict(inspect.getmembers(fn))
        result = {
            '__code__': cls.simplify_to_json_supported(getattr(fn, '__code__')),
            '__name__': cls.simplify_to_json_supported(getattr(fn, '__name__')),
            '__defaults__': cls.simplify_to_json_supported(getattr(fn, '__defaults__')),
            # '__closure__': cls.simplify_to_json_supported(getattr(fn, '__closure__')),
            # '__globals__': {}
        }
        fn_globals = {}
        for var in getattr(fn, '__code__').co_names:
            if var in getattr(fn, '__globals__'):
                fn_globals[var] = cls.simplify_to_json_supported(getattr(fn, '__globals__')[var])
        result['__globals__'] = fn_globals
        return result

    @classmethod
    def _simplify_complex(cls, complex_obj: object):
        # members = dict(inspect.getmembers(complex_obj))
        members = dict(filter(lambda member: not hasattr(member[1], '__call__') and member[0] != '__doc__',
                              inspect.getmembers(complex_obj)))
        # members = dict(filter(lambda member: inspect.isbuiltin(member[1]), inspect.getmembers(complex_obj)))
        # types
        return cls.simplify_to_json_supported(members)


class Constructor:

    @classmethod
    def construct_object(cls, data):
        # if isinstance(data, (type(None), int, float, str, list, tuple, bytes, set)):
        if not isinstance(data, dict) or '__code__' not in data:
            return cls._construct_simple(data)
        elif '__code__' in data:
            return cls._construct_function(data)

    @classmethod
    def _construct_function(cls, data: dict):
        vars_code = data['__code__']
        fn_code = types.CodeType(
            vars_code['co_argcount'],
            vars_code['co_posonlyargcount'],
            vars_code['co_kwonlyargcount'],
            vars_code['co_nlocals'],
            vars_code['co_stacksize'],
            vars_code['co_flags'],
            bytes(vars_code['co_code']),
            tuple(vars_code['co_consts']),
            tuple(vars_code['co_names']),
            tuple(vars_code['co_varnames']),
            vars_code['co_filename'],
            vars_code['co_name'],
            vars_code['co_firstlineno'],
            bytes(vars_code['co_lnotab']),
            tuple(vars_code['co_freevars']),
            tuple(vars_code['co_cellvars']),
        )

        fn_globals = data['__globals__']
        for key, val in fn_globals.items():
            fn_globals[key] = cls.construct_object(val)
        fn_globals['__builtins__'] = __builtins__
        # for var in vars_code.co_names:
        #     if var in getattr(fn, '__globals__'):
        fn_name = data['__name__']
        fn_defaults = data['__defaults__']
        if isinstance(fn_defaults, list):
            fn_defaults = tuple(fn_defaults)
        return types.FunctionType(
            code=fn_code,
            globals=fn_globals,
            name=fn_name,
            argdefs=fn_defaults
        )

    @classmethod
    def _construct_object(cls, data: dict):
        raise NotImplementedError

    @classmethod
    def _construct_simple(cls, data):
        return data

# CONST = 5
#
#
# def fn_hren(y=10):
#     return y
#

# def fn_test(x):
#     x += CONST
#     x = pow(x, 2)
#     return x + fn_hren()
#
#
# class ClassTest:
#     def __init__(self):
#         pass
#
#     x = CONST
#
#     def meth(self, y):
#         self.x += y
#         return self.x

#
# # obj = {'nine': 9, 'list': [5, 8, None], b'sad': bytes([4, 2, 19, 123]), '1': b'sad'}
# # print(obj)
# # res = serialize_obj(obj)
# inst = ClassTest()
# res_ser = Simplifier.simplify_to_json_supported(fn_test)
# # res = Simplifier.simplify_to_json_supported(inst)
# # res = Simplifier.simplify_to_json_supported(ClassTest)
# print(res_ser)
# res_deser = Constructor.construct_object(res_ser)
# print(res_deser)
# print(res_deser(15))
# # x = b'asf'
# # res = Simplifier.simplify_to_json_supported({x: 6})
