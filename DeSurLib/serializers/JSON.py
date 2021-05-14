import json

from DeSurLib.interfaces import Serializer
from DeSurLib.utils import Simplifier, Constructor


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
