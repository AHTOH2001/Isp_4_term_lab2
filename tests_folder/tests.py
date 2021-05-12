import unittest
import logging

from serializers import factory, interfaces
import os
from abc import abstractmethod
import tests_folder.testsHelper as testsHelper


# import bin.DeSur


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
        raise unittest.SkipTest('Class serialization currently does not work')
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
        init_data = {'nine': 9, 'list': [5, 8, 6]}

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

    def test_function_in_dict(self):
        # init_data = {5: 9, 'x': {'y': {testsHelper.fn_test}}, 'cless': testsHelper.ClassTest}
        init_data = {'5': 9, 'x': {'y': {testsHelper.fn_test}}}

        with open('test_complex.txt', self.write_type) as fp:
            self.suspect.dump(init_data, fp)

        with open('test_complex.txt', self.read_type) as fp:
            data = self.suspect.load(fp)
            # self.assertEqual(data, init_data)
            self.assertEqual(list(data['x']['y'])[0](5), 110)
            # inst = data['cless']()
            # self.assertEqual(inst.x, 5)
            # self.assertEqual(inst.meth(-5), 0)
            # self.assertEqual(inst.x, 0)

        with open('test_complex.txt', self.read_type) as fp:
            data = self.suspect.loads(fp.read())
            self.assertEqual(list(data['x']['y'])[0](5), 110)
            # self.assertEqual(data, init_data)

        with open('test_complex.txt', self.read_type) as fp:
            self.assertEqual(self.suspect.dumps(init_data), fp.read())

    def test_instance(self):
        raise unittest.SkipTest('Class serialization currently does not work')
        init_data = testsHelper.ClassTest()

        with open('test_inst.txt', self.write_type) as fp:
            self.suspect.dump(init_data, fp)

        with open('test_inst.txt', self.read_type) as fp:
            data = self.suspect.load(fp)
            # self.assertEqual(data, init_data)
            self.assertEqual(data.meth(15), 20)
            self.assertEqual(data.x, 20)

        with open('test_inst.txt', self.read_type) as fp:
            data = self.suspect.loads(fp.read())
            # self.assertEqual(data, init_data)

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
        if os.path.exists('test_inst.txt'):
            os.remove('test_inst.txt')


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
        self.suspect = factory.create_serialzer('Pickle')
        self.write_type = self.suspect.write_type
        self.read_type = self.suspect.read_type


class TestDeSurExecuter(unittest.TestCase):

    def setUp(self):
        self.init_data = {'5': 9, 'x': {'y': {testsHelper.fn_test}}}
        self.first_serializer = 'json'
        self.inst_ser = factory.create_serialzer(self.first_serializer)

        with open(f'test_console.{self.first_serializer}', self.inst_ser.write_type) as fp:
            self.inst_ser.dump(self.init_data, fp)

    def test_to_json(self):
        os.system(f'python bin/DeSur.py --json test_console.{self.first_serializer}')

        json_ser = factory.create_serialzer('json')
        expected_res = json_ser.dumps(self.init_data)

        with open(f'test_console.json', json_ser.read_type) as fp:
            actual_res = fp.read()

        self.assertEqual(expected_res, actual_res)

    def test_to_yaml(self):
        os.system(f'python bin/DeSur.py --yaml test_console.{self.first_serializer}')

        yaml_ser = factory.create_serialzer('yaml')
        expected_res = yaml_ser.dumps(self.init_data)

        with open(f'test_console.yaml', yaml_ser.read_type) as fp:
            actual_res = fp.read()

        self.assertEqual(expected_res, actual_res)

    def test_to_toml(self):
        os.system(f'python bin/DeSur.py --toml test_console.{self.first_serializer}')

        toml_ser = factory.create_serialzer('toml')
        expected_res = toml_ser.dumps(self.init_data)

        with open(f'test_console.toml', toml_ser.read_type) as fp:
            actual_res = fp.read()

        self.assertEqual(expected_res, actual_res)

    def test_to_pickle(self):
        os.system(f'python bin/DeSur.py --pickle test_console.{self.first_serializer}')

        pickle_ser = factory.create_serialzer('pickle')
        expected_res = pickle_ser.dumps(self.init_data)

        with open(f'test_console.pickle', pickle_ser.read_type) as fp:
            actual_res = fp.read()

        self.assertEqual(expected_res, actual_res)

    def test_all_console_serializations(self):
        # raise unittest.SkipTest('Class serialization currently does not work')
        with open(f'test_console.{self.first_serializer}', self.inst_ser.read_type) as fp:
            init_serialized_data = fp.read()

        os.system(f'python bin/DeSur.py --yaml test_console.{self.first_serializer}')
        os.system(f'python bin/DeSur.py --toml test_console.yaml')
        os.system(f'python bin/DeSur.py --json test_console.toml')
        os.system(f'python bin/DeSur.py --pickle test_console.json')
        os.system(f'python bin/DeSur.py --{self.first_serializer} test_console.pickle')

        with open(f'test_console.{self.first_serializer}', self.inst_ser.read_type) as fp:
            res_serialized_data = fp.read()

        self.assertEqual(init_serialized_data, res_serialized_data)

    def test_double_ser(self):
        # raise unittest.SkipTest('Class serialization currently does not work')
        os.system(f'python bin/DeSur.py --{self.first_serializer} test_console.{self.first_serializer}')

    # @classmethod
    def tearDown(self):
        pass
        for address, dirs, files in os.walk('.'):
            for file in files:
                if 'test_console' in file:
                    os.remove(file)


if __name__ == '__main__':
    unittest.main()
