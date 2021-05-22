import toml

from DeSurLib.interfaces import Serializer
from DeSurLib.utils import Simplifier, Constructor
from DeSurLib.exceptions import SerializationException, DeSerializationException


class TOML(Serializer):
    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def dumps(self, obj) -> str:
        dct = Simplifier.simplify_to_json_supported(obj)
        try:
            return toml.dumps(dct)
        except toml.TomlDecodeError as e:
            raise SerializationException(e)

    def load(self, fp):
        return self.loads(fp.read())

    def loads(self, s):
        try:
            obj = Constructor.construct_object(toml.loads(s))
        except (toml.TomlDecodeError, ValueError) as e:
            raise DeSerializationException(e)
        return obj
