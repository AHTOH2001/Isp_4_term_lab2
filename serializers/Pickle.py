import pickle

from serializers.interfaces import Serializer
from serializers.utils import Simplifier, Constructor


class Pickle(Serializer):
    """Binary (wb, rb)"""
    write_type = 'wb'
    read_type = 'rb'

    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def dumps(self, obj):
        dct = Simplifier.simplify_to_json_supported(obj)
        return pickle.dumps(dct, protocol=0)

    def load(self, fp):
        return self.loads(fp.read())

    def loads(self, s):
        obj = Constructor.construct_object(pickle.loads(s))
        return obj
