from interfaces import Serializer

import pickle


class Pickle(Serializer):
    """Binary (wb, rb)"""

    def dump(self, obj, fp):
        pickle.dump(obj, fp, protocol=0)

    def dumps(self, obj):
        return pickle.dumps(obj, protocol=0)

    def load(self, fp):
        return pickle.load(fp)

    def loads(self, s):
        return pickle.loads(s)
