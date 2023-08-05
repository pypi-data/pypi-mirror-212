from Xml_serialiser import serialiser_XML
from Json_serialiser import serialiser_JSON

class Serializer_fabric:

    @staticmethod
    def create_serializer(format_name: str):
        format_name = format_name.lower()

        if (format_name == "xml"):
            return serialiser_XML()
        elif(format_name == "json"):
            return serialiser_JSON()
        else:
            raise ValueError