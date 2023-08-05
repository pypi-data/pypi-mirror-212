from lab3.constants import JSON, XML
from lab3 import Json, xml


class Serializer:

    @staticmethod
    def create_serializer(t):
        if t == JSON:
            return Json
        if t == XML:
            return xml

        else:
            raise ValueError
