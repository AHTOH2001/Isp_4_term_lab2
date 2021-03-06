import unittest
import pickle

import os
from abc import abstractmethod

import tests_folder.victims_for_tests as victims
from DeSurLib import utils, fabric, interfaces, exceptions


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
        init_data = victims.ClassTest

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
        init_data = {'5': 9, 'x': {'y': [victims.fn_with_pow_and_sf]}}

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

    def test_function_with_builtin(self):
        init_data = victims.fn_with_builtin

        with open('test_builtin.txt', self.write_type) as fp:
            try:
                self.suspect.dump(init_data, fp)
            except exceptions.SerializationException:
                pass
            else:
                raise exceptions.SerializationException('Exception was not rised')

        try:
            self.suspect.dumps(init_data)
        except exceptions.SerializationException:
            pass
        else:
            raise exceptions.SerializationException('Exception was not rised')

    def test_instance(self):
        raise unittest.SkipTest('Class serialization currently does not work')
        init_data = victims.ClassTest()

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
        init_data = victims.fn_with_pow_and_sf

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

    def test_rec_func(self):
        init_data = victims.fibonachi

        with open('test_rec_func.txt', self.write_type) as fp:
            self.suspect.dump(init_data, fp)

        with open('test_rec_func.txt', self.read_type) as fp:
            data = self.suspect.load(fp)
            # self.assertEqual(data, init_data)
            self.assertEqual(data(6), 8)

        with open('test_rec_func.txt', self.read_type) as fp:
            data = self.suspect.loads(fp.read())
            self.assertEqual(data(7), 13)
            # self.assertEqual(data, init_data)

        with open('test_rec_func.txt', self.read_type) as fp:
            self.assertEqual(self.suspect.dumps(init_data), fp.read())

    def test_error_in_serialized(self):
        # raise unittest.SkipTest()
        init_data = {'x': [4, 6, 8]}

        ser_data = self.suspect.dumps(init_data)

        try:
            if self.write_type == 'wb':
                self.suspect.loads(ser_data[:10])
            else:
                self.suspect.loads(ser_data + 'chupakabra')
        except exceptions.DeSerializationException:
            pass
        else:
            raise exceptions.DeSerializationException('Exception was not rised')

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
        if os.path.exists('test_rec_func.txt'):
            os.remove('test_rec_func.txt')
        if os.path.exists('test_builtin.txt'):
            os.remove('test_builtin.txt')


class TestJSON(SerializerTestCase):
    def setUp(self):
        self.suspect = fabric.create_serialzer('JSON')


class TestYAML(SerializerTestCase):
    def setUp(self):
        self.suspect = fabric.create_serialzer('YAML')


class TestTOML(SerializerTestCase):
    def setUp(self):
        self.suspect = fabric.create_serialzer('TOML')


class TestPickle(SerializerTestCase):
    def setUp(self):
        self.suspect = fabric.create_serialzer('Pickle')
        self.write_type = self.suspect.write_type
        self.read_type = self.suspect.read_type


class TestDeSurExecuter(unittest.TestCase):

    def setUp(self):
        # self.init_data = {'5': 9, 'x': {'y': {testsHelper.fn_test}}}
        self.init_data = victims.fn_with_pow_and_sf
        self.first_serializer = 'toml'
        self.inst_ser = fabric.create_serialzer(self.first_serializer)

        with open(f'test_console.{self.first_serializer}', self.inst_ser.write_type) as fp:
            self.inst_ser.dump(self.init_data, fp)

    def test_to_json(self):
        os.system(f'python bin/DeSur.py --json test_console.{self.first_serializer}')

        json_ser = fabric.create_serialzer('json')
        expected_res = json_ser.dumps(self.init_data)

        with open(f'test_console.json', json_ser.read_type) as fp:
            actual_res = fp.read()

        self.assertEqual(expected_res, actual_res)

    def test_to_yaml(self):
        os.system(f'python bin/DeSur.py --yaml test_console.{self.first_serializer}')

        yaml_ser = fabric.create_serialzer('yaml')
        expected_res = yaml_ser.dumps(self.init_data)

        with open(f'test_console.yaml', yaml_ser.read_type) as fp:
            actual_res = fp.read()

        self.assertEqual(expected_res, actual_res)

    def test_to_toml(self):
        os.system(f'python bin/DeSur.py --toml test_console.{self.first_serializer}')

        toml_ser = fabric.create_serialzer('toml')
        expected_res = toml_ser.dumps(self.init_data)

        with open(f'test_console.toml', toml_ser.read_type) as fp:
            actual_res = fp.read()

        self.assertEqual(expected_res, actual_res)

    def test_to_pickle(self):
        os.system(f'python bin/DeSur.py --pickle test_console.{self.first_serializer}')

        pickle_ser = fabric.create_serialzer('pickle')
        expected_res = pickle_ser.dumps(self.init_data)

        with open(f'test_console.pickle', pickle_ser.read_type) as fp:
            actual_res = fp.read()

        # self.assertEqual(expected_res, actual_res)
        obj1 = utils.Simplifier.simplify_to_json_supported(pickle_ser.loads(expected_res))
        obj2 = utils.Simplifier.simplify_to_json_supported(pickle_ser.loads(actual_res))
        self.assertEqual(obj1, obj2)

    def test_interesting(self):
        # pickle_ser = factory.create_serialzer('pickle')
        yaml_ser = fabric.create_serialzer('yaml')
        double_ser_obj = yaml_ser.loads(yaml_ser.dumps(self.init_data))
        simple_init_obj = utils.Simplifier.simplify_to_json_supported(self.init_data)
        simple_double_obj = utils.Simplifier.simplify_to_json_supported(double_ser_obj)
        self.assertEqual(simple_init_obj, simple_double_obj)
        pickle_ser_init = pickle.dumps(simple_init_obj)
        pickle_ser_double = pickle.dumps(simple_double_obj)
        simple_deser_init = pickle.loads(pickle_ser_init)
        simple_deser_double = pickle.loads(pickle_ser_double)
        self.assertEqual(simple_deser_init, simple_deser_double)
        self.assertNotEqual(pickle_ser_init, pickle_ser_double)

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
        res = os.system(f'python bin/DeSur.py --{self.first_serializer} test_console.{self.first_serializer}')
        self.assertEqual(256, res)

    def test_nonexistent_file(self):
        res = os.system(f'python bin/DeSur.py --yaml nonexistent_file.toml')
        self.assertEqual(256, res)

    def test_wrong_format_file(self):
        res = os.system(f'python bin/DeSur.py --yaml test_console.dejavu')
        self.assertEqual(256, res)

    def test_wrong_format_ser(self):
        res = os.system(f'python bin/DeSur.py --hithere test_console.{self.first_serializer}')
        self.assertEqual(512, res)

    def tearDown(self):
        pass
        for address, dirs, files in os.walk('.'):
            for file in files:
                if 'test_console' in file:
                    os.remove(file)


if __name__ == '__main__':
    unittest.main()
