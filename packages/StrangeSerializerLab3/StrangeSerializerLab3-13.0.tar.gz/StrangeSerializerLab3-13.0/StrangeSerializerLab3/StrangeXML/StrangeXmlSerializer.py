from StrangeSerializerLab3.AdditionalFunctions import serialize, deserialize
from StrangeSerializerLab3.StrangeXML.parser import dumps_from_dict


class StrangeXmlSerializer:
    @staticmethod
    def dump(obj, file_name):
        with open(file_name, 'w') as file:
            file.write(StrangeXmlSerializer.dumps(obj))

    @staticmethod
    def dumps(obj):
        return dumps_from_dict(serialize(obj))

    @staticmethod
    def load(file_name):
        with open(file_name, 'r') as file:
            return StrangeXmlSerializer.loads(file.read())

    @staticmethod
    def loads(str_tmp):
        return deserialize(str_tmp)
