# import json

from DeSurLib.interfaces import Serializer
from DeSurLib.utils import Simplifier, Constructor
from DeSurLib.exceptions import SerializationException, DeSerializationException


class JSON(Serializer):

    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def dumps(self, obj) -> str:
        dct = Simplifier.simplify_to_json_supported(obj)
        return str(dct).replace("'", '"').replace('(', '[').replace(')', ']').replace(
            'None', 'null').replace('False', 'false').replace('True', 'true')
        # return json.dumps(dct)

    def load(self, fp):
        return self.loads(fp.read())

    def loads(self, s):
        try:
            obj = Constructor.construct_object(
                eval(s.replace('null', 'None').replace('false', 'False').replace('true', 'True')))
        except SyntaxError as e:
            raise DeSerializationException(e)
        # obj = Constructor.construct_object(json.loads(s))
        return obj
