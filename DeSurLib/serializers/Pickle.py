import pickle

from DeSurLib.interfaces import Serializer
from DeSurLib.utils import Simplifier, Constructor
from DeSurLib.exceptions import SerializationException, DeSerializationException


class Pickle(Serializer):
    """Binary (wb, rb)"""
    write_type = 'wb'
    read_type = 'rb'

    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def dumps(self, obj):
        dct = Simplifier.simplify_to_json_supported(obj)
        try:
            return pickle.dumps(dct, protocol=0)
        except pickle.PicklingError as e:
            raise SerializationException(e)

    def load(self, fp):
        return self.loads(fp.read())

    def loads(self, s):
        try:
            obj = Constructor.construct_object(pickle.loads(s))
        except pickle.UnpicklingError as e:
            raise DeSerializationException(e)
        return obj
