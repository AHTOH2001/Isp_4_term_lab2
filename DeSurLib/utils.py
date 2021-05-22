import inspect
import types
import logging
from .exceptions import SerializationException


class Simplifier:

    @classmethod
    def simplify_to_json_supported(cls, obj: object):
        if isinstance(obj, (type(None), int, float, str, list, tuple, bytes, dict, set)):
            return cls._simplify_simple(obj)
        elif inspect.isfunction(obj):
            return cls._simplify_function(obj)
        elif inspect.isclass(obj):
            raise SerializationException('Class serialization currently does not work')
        elif inspect.ismodule(obj):
            raise SerializationException('Module serialization currently does not work')
        else:
            return cls._simplify_complex(obj)

    @classmethod
    def _simplify_simple(cls, simple_obj: object):
        if isinstance(simple_obj, bytes):
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
        result = {
            '__code__': cls.simplify_to_json_supported(getattr(fn, '__code__')),
            '__name__': cls.simplify_to_json_supported(getattr(fn, '__name__')),
            '__defaults__': cls.simplify_to_json_supported(getattr(fn, '__defaults__')),
        }
        result['__code__']['co_consts'].pop(0)
        fn_globals = {}
        for var in getattr(fn, '__code__').co_names:
            if var in getattr(fn, '__globals__'):
                if var == result['__name__']:
                    fn_globals[var] = 'self'
                else:
                    if inspect.ismodule(getattr(fn, '__globals__')[var]):
                        raise SerializationException('Module cannot be serialized')
                    fn_globals[var] = cls.simplify_to_json_supported(getattr(fn, '__globals__')[var])
        result['__globals__'] = fn_globals
        return result

    @classmethod
    def _simplify_complex(cls, complex_obj: object):
        # members = dict(inspect.getmembers(complex_obj))
        members = dict(filter(lambda member: not hasattr(member[1], '__call__') and member[0] != '__doc__',
                              inspect.getmembers(complex_obj)))
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
            tuple([None] + vars_code['co_consts']),
            tuple(vars_code['co_names']),
            tuple(vars_code['co_varnames']),
            vars_code['co_filename'],
            vars_code['co_name'],
            vars_code['co_firstlineno'],
            bytes(vars_code['co_lnotab']),
            tuple(vars_code['co_freevars']),
            tuple(vars_code['co_cellvars']),
        )

        if '__globals__' not in data:
            fn_globals = {}
        else:
            fn_globals = data['__globals__']
        for key, val in fn_globals.items():
            fn_globals[key] = cls.construct_object(val)
        fn_globals['__builtins__'] = __builtins__
        fn_name = data['__name__']
        if '__defaults__' not in data:
            fn_defaults = None
        else:
            fn_defaults = data['__defaults__']
        if isinstance(fn_defaults, list):
            fn_defaults = tuple(fn_defaults)

        res_func = types.FunctionType(
            code=fn_code,
            globals=fn_globals,
            name=fn_name,
            argdefs=fn_defaults
        )
        if 'self' in res_func.__globals__.values():
            res_func.__globals__[res_func.__name__] = res_func

        return res_func

    @classmethod
    def _construct_object(cls, data: dict):
        raise NotImplementedError

    @classmethod
    def _construct_simple(cls, data):
        if isinstance(data, (str, int, bool, type(None), float)):
            return data
        elif isinstance(data, list):
            return [cls.construct_object(el) for el in data]
        elif isinstance(data, dict):
            return dict(
                [(cls.construct_object(key), cls.construct_object(val)) for key, val in
                 data.items()])
        else:
            return data
