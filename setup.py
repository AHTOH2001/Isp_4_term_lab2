from setuptools import setup, find_packages

setup(
    name='DeSur',
    version='0.1',
    packages=find_packages(),
    description='Custom serializer for json, toml, yaml, pickle that supports function serialization',
    author='AHTOH2001',
    url='https://github.com/AHTOH2001',
    install_requires=['toml', 'PyYAML'],
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest'],
    # test_suite='tests',
    scripts=['bin/DeSur']
)
