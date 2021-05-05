from interfaces import Serializer
import json
import yaml
import toml
import pickle

import inspect


class JSON(Serializer):

    def dump(self, obj, fp):
        if inspect.isclass(obj):
            raise Exception('class')
        if inspect.isfunction(obj):
            raise Exception('func')

        json.dump(obj, fp)

    def dumps(self, obj) -> str:
        return json.dumps(obj)

    def load(self, fp):
        return json.load(fp)

    def loads(self, s):
        return json.loads(s)


class YAML(Serializer):
    def dump(self, obj, fp):
        yaml.dump(obj, fp)

    def dumps(self, obj) -> str:
        return yaml.dump(obj)

    def load(self, fp):
        return yaml.load(fp, Loader=yaml.FullLoader)

    def loads(self, s):
        return yaml.load(s, Loader=yaml.FullLoader)


class TOML(Serializer):
    def dump(self, obj, fp):
        toml.dump(obj, fp)

    def dumps(self, obj) -> str:
        return toml.dumps(obj)

    def load(self, fp):
        return toml.load(fp)

    def loads(self, s):
        return toml.loads(s)


class Pickle(Serializer):
    """Binary (wb, rb)"""

    def dump(self, obj, fp):
        pickle.dump(obj, fp)

    def dumps(self, obj):
        return pickle.dumps(obj)

    def load(self, fp):
        return pickle.load(fp)

    def loads(self, s):
        return pickle.loads(s)
