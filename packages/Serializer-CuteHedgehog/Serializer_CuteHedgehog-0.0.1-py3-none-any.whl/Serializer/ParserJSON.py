import Serializer.SerializerJSON
import Serializer.DeserializerJSON


class JsonParser:

    @staticmethod
    def dump(obj, filename, indent=0):
        result = JsonParser.dumps(obj, indent)
        with open(filename, 'w') as file:
            file.write(result)

    @staticmethod
    def dumps(obj, indent=0) -> str:
        result = Serializer.SerializerJSON.serialize(obj, indent)
        return result

    @staticmethod
    def load(filename):
        with open(filename, 'r') as file:
            data = file.read()
        result = JsonParser.loads(data)
        return result

    @staticmethod
    def loads(data: str):
        result = Serializer.DeserializerJSON.deserialize(data)[0]
        return result
