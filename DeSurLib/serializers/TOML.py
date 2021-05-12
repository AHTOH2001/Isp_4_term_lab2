import toml
# import pytomlpp as toml
from DeSurLib.interfaces import Serializer
from DeSurLib.utils import Simplifier, Constructor


class TOML(Serializer):
    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def dumps(self, obj) -> str:
        dct = Simplifier.simplify_to_json_supported(obj)
        return toml.dumps(dct)

    def load(self, fp):
        return self.loads(fp.read())

    def loads(self, s):
        obj = Constructor.construct_object(toml.loads(s))
        return obj
