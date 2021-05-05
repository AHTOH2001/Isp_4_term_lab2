from interfaces import Serializer

import inspect
import json


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if not inspect.isbuiltin(obj):
                module = inspect.getmodule(obj)
                if module is not None:
                    JSON.code += inspect.getsource(module) + '\n'
                    return module.__name__ + '.' + obj.__name__
        except OSError:
            pass

        if isinstance(obj, set):
            return '{' + ', '.join((self.default(e) for e in obj)) + '}'

        return json.JSONEncoder.default(self, obj)


class JSON(Serializer):
    code = ''

    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def dumps(self, obj) -> str:
        JSON.code = ''
        res = json.dumps(obj, cls=MyEncoder)  # dumps will change JSON.code
        return JSON.code + '\n*CodeEnd*\n' + res

    def load(self, fp):
        return json.load(fp)

    def loads(self, s):
        return json.loads(s)
