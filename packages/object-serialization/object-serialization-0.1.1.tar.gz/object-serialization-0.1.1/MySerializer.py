import json_helper
import xml_helper


class MySerializer:
    @staticmethod
    def createSerializer(type):
        return MySerializer(type)

    def __init__(self, type):
        if type == '.xml':
            self.dumps = xml_helper.full_serialization
            self.dump = xml_helper.write
            self.loads = xml_helper.full_deserialization
            self.load = xml_helper.read

        elif type == '.json':
            self.dumps = json_helper.full_serialization
            self.dump = json_helper.write
            self.loads = json_helper.full_deserialization
            self.load = json_helper.read


