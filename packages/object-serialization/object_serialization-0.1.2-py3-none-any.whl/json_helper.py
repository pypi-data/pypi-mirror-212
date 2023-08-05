from serialization_helper import serialize_all, deserialize_all


def serialized_to_json(obj):
    result = ""
    if isinstance(obj, str):
        result = '\'' + obj + '\''
    elif isinstance(obj, type(None)):
        result = 'null'
    elif isinstance(obj, (int, float, bool)):
        result = str(obj)
    elif isinstance(obj, list):
        result = '['
        for val in obj:
            if result != '[':
                result += ', '
            result += serialized_to_json(val)
        result += ']'
    elif isinstance(obj, dict):
        result = '{'
        for name, val in obj.items():
            if result != '{':
                result += ', '
            result += serialized_to_json(name)
            result += ': '
            result += serialized_to_json(val)
        result += '}'
    return result


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_int(string):
    return string.isdigit()


def json_to_serialized(data):
    if data == 'null':
        return None
    elif data[0] == '\'' and data[-1] == '\'':
        return data[1:-1]
    elif is_int(data):
        return int(data)
    elif is_float(data):
        return float(data)
    elif data == 'True':
        return True
    elif data == 'False':
        return False
    elif data[0] == '[' and data[-1] == ']':
        result = []
        index = 1
        while index < len(data):
            if data[index] in ['[', '{', '\'']:
                if data[index] == '[':
                    left = '['
                    right = ']'
                if data[index] == '{':
                    left = '{'
                    right = '}'
                if data[index] == '\'':
                    left = ''
                    right = '\''
                edge_count = 1
                substr = data[index]
                index += 1
                while edge_count > 0:
                    substr += data[index]
                    if data[index] == left:
                        edge_count += 1
                    if data[index] == right:
                        edge_count -= 1
                    index += 1
            else:
                substr = ''
                while data[index] not in [',', ']']:
                    substr += data[index]
                    index += 1

            result.append(json_to_serialized(substr))

            index += 2  # ", " symbols
        return result

    elif data[0] == '{' and data[-1] == '}':
        result = {}
        index = 2
        while index < len(data):
            name = ''
            while data[index] != '\'':
                name += data[index]
                index += 1
            index += 3  # "': "

            if data[index] in ['[', '{', '\'']:
                if data[index] == '[':
                    left = '['
                    right = ']'
                if data[index] == '{':
                    left = '{'
                    right = '}'
                if data[index] == '\'':
                    left = ''
                    right = '\''
                edge_count = 1
                substr = data[index]
                index += 1
                while edge_count > 0:
                    substr += data[index]
                    if data[index] == left:
                        edge_count += 1
                    if data[index] == right:
                        edge_count -= 1
                    index += 1
            else:
                substr = ''
                while data[index] not in [',', '}']:
                    substr += data[index]
                    index += 1

            result[name] = json_to_serialized(substr)
            index += 3  # ", '" symbols
        return result

def full_serialization(obj):
    return serialized_to_json(serialize_all(obj))

def full_deserialization(obj):
    return deserialize_all(json_to_serialized(obj))

def write(obj, fp):
    with open(fp, 'w') as f:
        f.write(serialized_to_json(serialize_all(obj)))


def read(fp):
    with open(fp, 'r') as f:
        return deserialize_all(json_to_serialized(f.read()))

