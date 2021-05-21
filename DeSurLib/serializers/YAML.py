import yaml

from DeSurLib.interfaces import Serializer
from DeSurLib.utils import Simplifier, Constructor
from DeSurLib.exceptions import SerializationException, DeSerializationException


class YAML(Serializer):
    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def dumps(self, obj) -> str:
        dct = Simplifier.simplify_to_json_supported(obj)
        try:
            return yaml.dump(dct)
        except yaml.YAMLError as e:
            raise SerializationException(e)

    def load(self, fp):
        return self.loads(fp.read())

    def loads(self, s):
        try:
            obj = Constructor.construct_object(yaml.load(s, Loader=yaml.FullLoader))
        except yaml.YAMLError as e:
            raise DeSerializationException(e)
        return obj
