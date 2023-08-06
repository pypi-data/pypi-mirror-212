from enum import Enum

from serializers import SerializerXml
from serializers import SerializerJson


class SerializerType(Enum):
    JSON = "json"
    XML = "xml"


class SerializersFactory:
    @staticmethod
    def create_serializer(st: SerializerType):

        if st == SerializerType.JSON:
            return SerializerJson()

        elif st == SerializerType.XML:
            return SerializerXml()

        else:
            raise Exception("Unknown type of serialization")