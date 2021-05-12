from DeSurLib import serializers


def create_serialzer(name: str):
    if name.lower() == 'json':
        inst = serializers.JSON()
    elif name.lower() == 'yaml':
        inst = serializers.YAML()
    elif name.lower() == 'toml':
        inst = serializers.TOML()
    elif name.lower() == 'pickle':
        inst = serializers.Pickle()
    else:
        raise NameError

    return inst

#
# j = create_serialzer('JSON')
# y = create_serialzer('YAML')
# t = create_serialzer('TOML')
# p = create_serialzer('Pickle')
#
# suspect = create_serialzer('YAML')
