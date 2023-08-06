from StrangeSerializerLab3.AdditionalFunctions import serialize, deserialize
from StrangeSerializerLab3.StrangeJSON.parser import parse


class StrangeJsonSerializer:
    @staticmethod
    def dump(obj, file_name):
        with open(file_name, 'w') as file:
            file.write(StrangeJsonSerializer.dumps(obj))

    @staticmethod
    def dumps(obj):
        return str(serialize(obj))

    @staticmethod
    def load(file_name):
        with open(file_name, 'r') as file:
            return StrangeJsonSerializer.loads(file.read())

    @staticmethod
    def loads(str_tmp):
        return deserialize(parse(str_tmp))
