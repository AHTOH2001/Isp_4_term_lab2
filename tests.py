import unittest
import factory
import interfaces
import os
from abc import ABCMeta, abstractmethod, abstractproperty
import testsHelper
import inspect


class SerializerTestCase(unittest.TestCase):
    @property
    def suspect(self):
        try:
            self._suspect
        except AttributeError:
            raise NotImplementedError('`suspect` field must be implemented')

        return self._suspect

    @suspect.setter
    def suspect(self, value):
        if isinstance(value, interfaces.Serializer):
            self._suspect = value
        else:
            raise ValueError('field `suspect` must be a Serializer')

    write_type = 'w'
    read_type = 'r'

    @abstractmethod
    def setUp(self):
        raise unittest.SkipTest('Test called without `suspect` field')

    def test_class(self):
        init_data = testsHelper.ClassTest

        with open('test_class.txt', self.write_type) as fp:
            self.suspect.dump(init_data, fp)

        with open('test_class.txt', self.read_type) as fp:
            data = self.suspect.load(fp)
            self.assertEqual(data, init_data)
            inst = data()
            self.assertEqual(inst.x, 5)
            self.assertEqual(inst.meth(3), 8)
            self.assertEqual(inst.x, 8)

        with open('test_class.txt', self.read_type) as fp:
            data = self.suspect.loads(fp.read())
            self.assertEqual(data, init_data)

        with open('test_class.txt', self.read_type) as fp:
            self.assertEqual(self.suspect.dumps(init_data), fp.read())

    def test_simple_object(self):
        init_data = {'nine': 9, 'list': [5, 8, None]}

        with open('test_simple.txt', self.write_type) as fp:
            self.suspect.dump(init_data, fp)

        with open('test_simple.txt', self.read_type) as fp:
            data = self.suspect.load(fp)
            self.assertEqual(data, init_data)

        with open('test_simple.txt', self.read_type) as fp:
            data = self.suspect.loads(fp.read())
            self.assertEqual(data, init_data)

        with open('test_simple.txt', self.read_type) as fp:
            self.assertEqual(self.suspect.dumps(init_data), fp.read())

    def test_complex_object(self):
        init_data = {5: 9, 'x': {'y': {testsHelper.fn_test}}, 'cless': testsHelper.ClassTest}

        with open('test_complex.txt', self.write_type) as fp:
            self.suspect.dump(init_data, fp)

        with open('test_complex.txt', self.read_type) as fp:
            data = self.suspect.load(fp)
            self.assertEqual(data, init_data)
            self.assertEqual(list(data['x']['y'])[0](5), 110)
            inst = data['cless']()
            self.assertEqual(inst.x, 5)
            self.assertEqual(inst.meth(-5), 0)
            self.assertEqual(inst.x, 0)

        with open('test_complex.txt', self.read_type) as fp:
            data = self.suspect.loads(fp.read())
            self.assertEqual(data, init_data)

        with open('test_complex.txt', self.read_type) as fp:
            self.assertEqual(self.suspect.dumps(init_data), fp.read())

    def test_instance(self):
        init_data = testsHelper.ClassTest()

        with open('test_inst.txt', self.write_type) as fp:
            self.suspect.dump(init_data, fp)


        with open('test_inst.txt', self.read_type) as fp:
            data = self.suspect.load(fp)
            self.assertEqual(data, init_data)
            self.assertEqual(data.meth(15), 20)
            self.assertEqual(data.x, 20)

        with open('test_inst.txt', self.read_type) as fp:
            data = self.suspect.loads(fp.read())
            self.assertEqual(data, init_data)

        with open('test_inst.txt', self.read_type) as fp:
            self.assertEqual(self.suspect.dumps(init_data), fp.read())

    def test_func(self):
        init_data = testsHelper.fn_test

        with open('test_func.txt', self.write_type) as fp:
            self.suspect.dump(init_data, fp)

        with open('test_func.txt', self.read_type) as fp:
            data = self.suspect.load(fp)
            # self.assertEqual(data, init_data)
            self.assertEqual(data(15), 410)

        with open('test_func.txt', self.read_type) as fp:
            data = self.suspect.loads(fp.read())
            self.assertEqual(data(15), 410)
            # self.assertEqual(data, init_data)

        with open('test_func.txt', self.read_type) as fp:
            self.assertEqual(self.suspect.dumps(init_data), fp.read())

    @classmethod
    def tearDownClass(cls):
        pass
        if os.path.exists('test_class.txt'):
            os.remove('test_class.txt')
        if os.path.exists('test_complex.txt'):
            os.remove('test_complex.txt')
        if os.path.exists('test_func.txt'):
            os.remove('test_func.txt')
        if os.path.exists('test_simple.txt'):
            os.remove('test_simple.txt')


class TestJSON(SerializerTestCase):
    def setUp(self):
        self.suspect = factory.create_serialzer('JSON')


class TestYAML(SerializerTestCase):
    def setUp(self):
        self.suspect = factory.create_serialzer('YAML')


class TestTOML(SerializerTestCase):
    def setUp(self):
        self.suspect = factory.create_serialzer('TOML')


class TestPickle(SerializerTestCase):
    def setUp(self):
        self.write_type = 'wb'
        self.read_type = 'rb'
        self.suspect = factory.create_serialzer('Pickle')


if __name__ == '__main__':
    unittest.main()
