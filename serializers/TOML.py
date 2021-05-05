from interfaces import Serializer

import toml


class TOML(Serializer):
    def dump(self, obj, fp):
        toml.dump(obj, fp)

    def dumps(self, obj) -> str:
        return toml.dumps(obj)

    def load(self, fp):
        return toml.load(fp)

    def loads(self, s):
        return toml.loads(s)
