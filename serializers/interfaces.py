from abc import ABCMeta, abstractmethod


class Serializer:
    __metaclass__ = ABCMeta
    write_type = 'w'
    read_type = 'r'
    
    @abstractmethod
    def dump(self, obj, fp):
        raise NotImplementedError('`dump` must be implemented.')

    @abstractmethod
    def dumps(self, obj) -> str:
        raise NotImplementedError('`dumps` must be implemented.')

    @abstractmethod
    def load(self, fp):
        raise NotImplementedError('`load` must be implemented.')

    @abstractmethod
    def loads(self, s):
        raise NotImplementedError('`loads` must be implemented.')
