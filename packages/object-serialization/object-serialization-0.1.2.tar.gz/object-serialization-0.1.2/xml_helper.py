import re

from serialization_helper import serialize_all, deserialize_all


def serialized_to_xml(obj):
    result = ""
    if isinstance(obj, str):
        result = '<string>' + obj + '</string>'
    elif isinstance(obj, type(None)):
        result = '<null />'
    elif isinstance(obj, int):
        result = '<int>' + str(obj) + '</int>'
    elif isinstance(obj, float):
        result = '<float>' + str(obj) + '</float>'
    elif isinstance(obj, bool):
        result = '<bool>' + str(obj) + '</bool>'
    elif isinstance(obj, list):
        result = '<list>'
        for val in obj:
            result += "<item>" + serialized_to_xml(val) + "</item>"
        result += '</list>'
    elif isinstance(obj, dict):
        result = '<dict>'
        for name, val in obj.items():
            result += "<" + name + ">"
            result += serialized_to_xml(val)
            result += "</" + name + ">"
        result += '</dict>'
    return result


def xml_to_serialized(data):
    name = re.split(r"[<>]", data)[1]
    if name == "string":
        return data[len("<string>"):-len("</string>")]
    if name == "int":
        return int(data[len("<int>"):-len("</int>")])
    if name == "float":
        return float(data[len("<float>"):-len("</float>")])
    if name == "bool":
        temp = data[len("<bool>"):-len("</bool>")]
        if temp == 'True':
            return True
        if temp == 'False':
            return False
    if name == "null /":
        return None
    if name == "list":
        result = []
        data = data[len("<list>"):-len("</list>")]
        index = 0
        itemstr = ''
        depth = 0
        while index < len(data) - len("</item>") + 1:
            itemstr += data[index]
            if data[index:index + len("<item>")] == "<item>":
                depth += 1
            if data[index:index + len("</item>")] == "</item>":
                depth -= 1
                if depth == 0:
                    itemstr += data[index + 1:index + len("</item>")]
                    itemstr = itemstr[len("<item>"):-len("</item>")]
                    result.append(xml_to_serialized(itemstr))
                    itemstr = ''
                    index += len("</item>") - 1
            index += 1
        return result

    if name == "dict":
        result = {}
        data = data[len("<dict>"):-len("</dict>")]
        index = 0
        itemstr = ''
        # find key name
        keyname = ''
        depth = 0

        while index < len(data) - len("</"+keyname+">") + 1:
            if keyname == '':      # next keyname
                tempindex = index+1
                while data[tempindex] !='>':
                    keyname+=data[tempindex]
                    tempindex+=1
            itemstr += data[index]
            if data[index:index + len("<"+keyname+">")] == "<"+keyname+">":
                depth += 1
            if data[index:index + len("</"+keyname+">")] == "</"+keyname+">":
                depth -= 1
                if depth == 0:
                    itemstr += data[index + 1:index + len("</"+keyname+">")]
                    itemstr = itemstr[len("<"+keyname+">"):-len("</"+keyname+">")]
                    result[keyname]=(xml_to_serialized(itemstr))
                    itemstr = ''
                    index += len("</"+keyname+">") - 1
                    keyname = ''
            index += 1
        return result

def full_serialization(obj):
    return serialized_to_xml(serialize_all(obj))

def full_deserialization(obj):
    return deserialize_all(xml_to_serialized(obj))

def write(obj, fp):
    with open(fp, 'w') as f:
        f.write(serialized_to_xml(serialize_all(obj)))


def read(obj, fp):
    with open(fp, 'r') as f:
        return deserialize_all(xml_to_serialized(f.read()))
