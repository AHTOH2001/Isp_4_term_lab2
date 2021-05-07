from interfaces import Serializer

import inspect
import json
from utils import Simplifier, Constructor


# class MyEncoder(json.JSONEncoder):
#     def default(self, obj):
#         try:
#             if not inspect.isbuiltin(obj):
#                 module = inspect.getmodule(obj)
#                 if module is not None:
#                     JSON.code += inspect.getsource(module) + '\n'
#                     return module.__name__ + '.' + obj.__name__
#         except OSError:
#             pass
#
#         if isinstance(obj, set):
#             return '{' + ', '.join((self.default(e) for e in obj)) + '}'
#
#         return json.JSONEncoder.default(self, obj)


class JSON(Serializer):

    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def dumps(self, obj) -> str:
        dct = Simplifier.simplify_to_json_supported(obj)
        return json.dumps(dct)

    def load(self, fp):
        return self.loads(fp.read())

    def loads(self, s):
        obj = Constructor.construct_object(json.loads(s))
        return obj
