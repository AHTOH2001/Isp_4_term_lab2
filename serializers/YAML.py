from interfaces import Serializer

import yaml


class YAML(Serializer):
    def dump(self, obj, fp):
        yaml.dump(obj, fp)

    def dumps(self, obj) -> str:
        return yaml.dump(obj)

    def load(self, fp):
        return yaml.load(fp, Loader=yaml.FullLoader)

    def loads(self, s):
        return yaml.load(s, Loader=yaml.FullLoader)
