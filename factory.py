import serializers


def create_serialzer(name):
    if name == 'JSON':
        inst = serializers.JSON()
    elif name == 'YAML':
        inst = serializers.YAML()
    elif name == 'TOML':
        inst = serializers.TOML()
    elif name == 'Pickle':
        inst = serializers.Pickle()
    else:
        raise NameError

    return inst


j = create_serialzer('JSON')
y = create_serialzer('YAML')
t = create_serialzer('TOML')
p = create_serialzer('Pickle')

suspect = create_serialzer('YAML')
