import yaml

from serializers.interfaces import Serializer
from serializers.utils import Simplifier, Constructor


class YAML(Serializer):
    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def dumps(self, obj) -> str:
        dct = Simplifier.simplify_to_json_supported(obj)
        return yaml.dump(dct)

    def load(self, fp):
        return self.loads(fp.read())

    def loads(self, s):
        obj = Constructor.construct_object(yaml.load(s, Loader=yaml.FullLoader))
        return obj
